
from django.contrib.auth.models import AbstractUser
from django.db import models

from .user_manager import EmailBasedUserManager


class EmailBasedUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=1024)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = EmailBasedUserManager()
