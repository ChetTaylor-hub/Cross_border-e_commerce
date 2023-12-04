from django.db import models

# Create your models here.
# models.py

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields like name, device count, etc.

class Promotion(models.Model):
    parent = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='children')
    child = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='parent')

# models.py
class Billing(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

