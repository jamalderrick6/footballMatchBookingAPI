from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ADMIN = "AD"
    FAN = "FN"
    ROLES = [
        (ADMIN, "admin"),
        (FAN, "fan"),
    ]
    """User model."""
    username = models.CharField(max_length=100, unique=False)
    firstName = models.CharField(max_length=150)
    lastName = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    birthDate = models.CharField(max_length=50)
    role = models.CharField(
        max_length=2,
        choices=ROLES,
        default=FAN,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        managed = True
        db_table = 'auth_user'

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print(instance.__dict__)


