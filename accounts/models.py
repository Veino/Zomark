from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .managers import ZomarkUserManager

# Create your models here.

class ZomarkUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    profileImage = models.ImageField(upload_to="profile-images")
    isZomarkAdmin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ZomarkUserManager()

    def __str__(self):
        return self.email
