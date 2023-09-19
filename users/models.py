from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        if not email.endswith("@makingscience.com") and not extra_fields.get("is_superuser"):
            raise ValueError(_("You can only register with makingscience email"))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser True."))
        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        blank=True,
        null=True)
    email = models.EmailField(max_length=100, unique=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Profile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
