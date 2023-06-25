from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.models import BaseModel

from apps.users.managers import UserManager


class ProfileModel(BaseModel):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    age = models.IntegerField()

    class Meta:
        db_table = 'profile'


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE, related_name='user')
    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
