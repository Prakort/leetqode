from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with Google OAuth2 fields."""
    email = models.EmailField(unique=True)
    avatar = models.URLField(blank=True, null=True)
    google_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
