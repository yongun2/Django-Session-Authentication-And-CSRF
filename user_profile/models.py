from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=20, default='')
    nickname = models.CharField(max_length=20, default='')

    def __str__(self):
        return f"유저 {self.name} 닉네임 {self.nickname}"
