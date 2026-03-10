from datetime import timedelta

from django.db import models
from django.utils import timezone

from src.utils.dbOptions import (LINK_GENERATION_CATEGORIES, MAX_STR_LEN,
                                 MIN_STR_LEN, TINY_STR_LEN)
from src.utils.helpers import random_token


class GeneratedLink(models.Model):
    id = models.CharField(primary_key=True, default=random_token, editable=False)
    category = models.CharField(
        max_length=TINY_STR_LEN,
        choices=LINK_GENERATION_CATEGORIES,
        null=False,
        blank=False,
    )
    token = models.CharField(
        max_length=TINY_STR_LEN,
        null=False,
        blank=False,
    )
    link = models.URLField(
        max_length=MAX_STR_LEN, null=False, unique=True, editable=False, blank=False
    )
    expires_at = models.DateTimeField(
        null=True, blank=True, 
    )
    updatedBy = models.CharField(
        max_length=MIN_STR_LEN, default="dev", null=True, blank=True
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            now = timezone.now() 
            self.expires_at = now + timedelta(days=2)
            return super().save(*args, **kwargs)

    @property
    def expired(self):
        try:
            dt = self.expires_at - timezone.now()
            return True if dt.total_seconds() < 60 else False
        except Exception:
            print(f"Failed to get link expiration date")

    class _Meta:
        verbose_name_plural = "Generated Links"
        ordering = ["-createdAt"]

    def __str__(self):
        return f"{self.category} - {self.link}"
