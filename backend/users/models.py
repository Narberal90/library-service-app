from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _

from users.managers.user_manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("Email address"), unique=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
