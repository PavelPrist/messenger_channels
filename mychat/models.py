from django.db import models
from django.contrib.auth.models import User


class UserCustom(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )


class Message(models.Model):
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
