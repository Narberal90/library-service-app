from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    email = models.EmailField(_("Email address"), unique=True)
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    password = models.CharField(_("Password"), max_length=255)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()