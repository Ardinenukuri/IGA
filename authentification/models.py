from django.contrib.auth.models import AbstractUser, Group
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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == self.CREATOR:
            group = Group.objects.get(name='creators')
            group.user_set.add(self)
        elif self.role == self.SUBSCRIBER:
            group = Group.objects.get(name='subscribers')
            group.user_set.add(self)
    
    follows = models.ManyToManyField(
        'self',
        limit_choices_to={'role': CREATOR},
        symmetrical=False
    )