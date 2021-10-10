from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.CharField(max_length=255,unique=True)
    password =  models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Utilisateur(models.Model):
    firstname = models.CharField(max_length=70, blank=False, default='')
    secondname = models.CharField(max_length=70,blank=False, default='')
    description = models.CharField(max_length=20, blank=False, default='')
    published = models.BooleanField(default=False)