from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from allauth.account.signals import user_logged_in

from apps.user.utils.converter import resizeConverter
from apps.user.utils.providerList import get_provider_url

from core.settings import allauth

User = get_user_model()

@receiver(post_save, sender=User, dispatch_uid="send_welcome_email")
def send_welcome_mail(sender, instance, created, **kwargs):
    """
    Send welcome email only if user is newly created.
    Handles exceptions to prevent login breaking.
    """
    if created and instance.email and instance.email != allauth.DEFAULT_FROM_EMAIL:
        subject = f"Welcome! {instance.username}"
        message = "Thanks for signing up on MAMA'D For Kids"

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email='mamadforkids@gmail.com',
                recipient_list=[instance.email],
                fail_silently=False,
            )
            print(f"Welcome email sent to {instance.email}")
        except Exception as e:
            # Catch SMTP errors (e.g., authentication) without breaking signup
            print(f"Failed to send welcome email to {instance.email}: {e}")
        
@receiver(user_logged_in)
def save_resized_avatar(request, user, **kwargs):
    if user.avatar:
        return
    
    url = get_provider_url(user)
    if url:
        resizeConverter(request, url)

@receiver(post_delete, sender=User)
def delete_user_avatar(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete(save=False)