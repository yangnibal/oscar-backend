from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import PermissionsMixin

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=10)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=1000)
    profile_img = models.ImageField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)
    followers = models.ManyToManyField('self', blank=True, symmetrical=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'is_staff', 'name']

    def __unicode__(self):
        return self.username

    objects = UserManager()



