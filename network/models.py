from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Class for New Form (possibly add mmore models or less models not sure yet)
class New_Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    comment_field = models.TextField(
        max_length=1000,
        help_text="Create a post! (1000 character limit!)",
        blank=False,
    )
