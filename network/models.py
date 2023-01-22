from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    timezone = models.CharField(
        max_length=255,
        blank=True,
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )

    def __str__(self):
        return self.username


# Class for New Form (possibly add mmore models or less models not sure yet)
class New_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    comment_field = models.TextField(
        max_length=1000,
        blank=False,
    )
    likes = models.ManyToManyField(User, related_name="like", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.comment_field
