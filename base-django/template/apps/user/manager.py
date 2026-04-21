from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        if extra_fields.get('user_type') == 'seller':
            extra_fields.setdefault('is_seller', True)
            user.custom_set_password(password, 'seller')
        else:
            extra_fields.setdefault('is_seller', False)
            user.custom_set_password(password, 'user')
             
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_seller', True)

        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_staff is True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser is True")
        
        return self.create_user(email, password, **extra_fields)
