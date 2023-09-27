from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,)
    email = models.EmailField(max_length=150, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    LEVEL = (
        ("junior", "Junior"),
        ("middle", "Middle"),
        ("senior", "Senior"),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    level = models.CharField(_("level"), choices=LEVEL, null=True)
    birth_date = models.DateField(_("birth date"), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)