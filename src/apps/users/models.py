from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager

from src.utils.dbOptions import *
from src.utils.helpers import random_token

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user_object(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, email, password, **extra_fields):
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("userType", "customer")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("userType", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    first_name = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    last_name = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=MIN_STR_LEN, null=False, blank=False)
    phone = models.CharField(max_length=MIN_STR_LEN, null=True, blank=True)
    userType = models.CharField(max_length=MIN_STR_LEN, default="customer", choices=USER_TYPES, null=True, blank=True)
    gender = models.CharField(max_length=TINY_STR_LEN, choices=GENDER, null=True, blank=True)
    createdBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    updatedBy = models.CharField(max_length=MIN_STR_LEN, default="dev", null=True, blank=True)
    createdAat = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class _Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} - {self.userType}"
