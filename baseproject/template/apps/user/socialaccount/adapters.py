import uuid

from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.text import slugify

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        if not user.username:
            email = data.get('email', '')
            username = slugify(email.split("@")[0])
            if User.objects.filter(username=username).exists():
                user.username = self.generate_unique_username(username)
            user.username = username
        return user
    
    def generate_unique_username(self, username):
        while True:
            suffix = uuid.uuid4().hex[:4]
            username = f"{username}_{suffix}"

            if not User.objects.filter(username=username).exists():
                return username