from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import os

class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return self.name


def cover_upload_path(instance, filename):
 
    platform_name = instance.platform.name.lower().replace(' ', '_')
    return os.path.join('covers', platform_name, filename)


class Game(models.Model):
    title = models.CharField(max_length=200)
    platform = models.ForeignKey(Platform, on_delete=models.RESTRICT)
    genre = models.ManyToManyField(Genre)
    age_rating = models.PositiveSmallIntegerField()
    cover_image = models.ImageField(upload_to=cover_upload_path, null=True, blank=True)
    description = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["platform"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.platform})"

    @property
    def available(self):
        return not self.loan_set.filter(returned_at__isnull=True).exists()


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    game = models.ForeignKey(Game, on_delete=models.RESTRICT)
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["game"]),
            models.Index(fields=["returned_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"],
                condition=models.Q(returned_at__isnull=True),
                name="unique_active_loan"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.pk and not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} -> {self.game} ({self.loan_date:%Y-%m-%d})"
