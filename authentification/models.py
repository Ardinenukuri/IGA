from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CREATOR = 'CREATOR'
    FOLLOWER = 'FOLLOWER'
  
    ROLE_CHOICES = (
        (CREATOR, 'Creator'),
        (FOLLOWER, 'follower'),
    )
    profile_photo = models.ImageField()
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)