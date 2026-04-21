from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.user.manager import CustomUserManager
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.


class User(AbstractUser):

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    email           = models.EmailField(unique=True)
    username        = models.CharField(max_length=150, unique=True)
    is_seller       = models.BooleanField(default=False)
    seller_password = models.CharField(max_length=128, blank=True)
    avatar          = models.ImageField(upload_to="avatars/", null=True, blank=True)

    objects = CustomUserManager()
    def custom_set_password(self, raw_password, user_type : str):
        hash_password = make_password(raw_password)

        if not user_type == "seller":
            self.password = hash_password
        else:
            self.seller_password = hash_password
       
    def custom_check_password(self, raw_password, user_type : str):
        if not user_type == "seller":
            return check_password(raw_password, self.password)
        else:
            return check_password(raw_password, self.seller_password)

