from django.contrib.auth.models import AbstractUser
from django.db import models

# class CustomUser(AbstractUser):
    # first_name = models.CharField(max_length=50, blank=False, null=False)
    # last_name = models.CharField(max_length=50, blank=False, null=False)
    # username = models.IntegerField(blank=False, null=False, unique=True)
    # password = models.CharField(blank=False, null=False, max_length=50)

    # def __str__(self):
    #     return f"{self.first_name} {self.last_name}"
    
class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, blank=False, null=False, unique=True)
    password = models.CharField(max_length=50, blank=False, null=False)
