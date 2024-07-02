from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
  username = models.CharField(max_length=150, unique=True)
  cnic = models.CharField(max_length=13, unique=True, null=False)
  phone_number = models.CharField(max_length=11, unique=True, null=False)
  email = models.EmailField(unique=True, null=False)

  USERNAME_FIELD = 'email'  # Set email as the unique identifier
  REQUIRED_FIELDS = ['username','first_name', 'last_name']

  # Add related_name arguments to avoid conflicts
  groups = models.ManyToManyField(
      'auth.Group',
      related_name='custom_users',
      blank=True,
      help_text='The groups this user belongs to. A user can belong to multiple groups.',
      verbose_name='groups'
  )
  user_permissions = models.ManyToManyField(
      'auth.Permission',
      related_name='custom_users',
      blank=True,
      help_text='Specific permissions for this user.',
      verbose_name='user permissions'
  )