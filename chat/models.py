from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return f'{self.username}'


class Thread(models.Model):
    participants = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(blank=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='threads')
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
