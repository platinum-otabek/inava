from django.contrib.auth.models import AbstractUser
from django.db import models

# Restoran va foydalanuvchi bitta
class CustomUser(AbstractUser):
    user = models.ForeignKey('CustomUser', on_delete=models.RESTRICT, default=None, null=True, blank=True)
    main_language = models.CharField(max_length=20, default=None, null=True, blank=True)
    name = models.CharField(max_length=100, default=None, null=True, blank=True)
    description = models.TextField(default=None, null=True, blank=True)
    currency = models.CharField(max_length=20, default=None, null=True, blank=True)
    location = models.TextField(default=None, null=True, blank=True)
    is_calculation = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='restaurant/', default=None, null=True, blank=True)
    is_restaurant = models.BooleanField(default=False)
    slug_name = models.SlugField(default=f'slug{id}', unique=True)


# chernovek
class SlugModel(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

