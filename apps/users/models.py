from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.db import models

from core.enums.regex_enum import RegExEnum
from core.models import BaseModel
from core.services.upload_avatar_service import upload_avatar

from apps.users.managers import UserManager


class ProfileModel(BaseModel):
    name = models.CharField(max_length=50, validators=(
        validators.RegexValidator(RegExEnum.NAME.pattern, RegExEnum.NAME.msg),
    ))
    surname = models.CharField(max_length=50, validators=(
        validators.RegexValidator(RegExEnum.SURNAME.pattern, RegExEnum.SURNAME.msg),
    ))
    age = models.IntegerField(validators=(
        validators.MinValueValidator(16),
        validators.MaxValueValidator(150)
    ))
    avatar = models.ImageField(upload_to=upload_avatar, blank=True)

    class Meta:
        db_table = 'profile'
        ordering = ('id', 'name', 'surname', 'age')


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True, validators=(
        validators.RegexValidator(RegExEnum.EMAIL.pattern, RegExEnum.EMAIL.msg),
    ))
    password = models.CharField(max_length=128, validators=(
        validators.RegexValidator(RegExEnum.PASSWORD.pattern, RegExEnum.PASSWORD.msg),
    ))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE, related_name='user', null=True)
    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        ordering = ('id',)
