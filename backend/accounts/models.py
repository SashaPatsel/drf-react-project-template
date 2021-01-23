from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

#  Lets us add custom fields to User model
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    regulator = models.BooleanField(default=False, null=True, blank=True)
    expert_badge = models.BooleanField(default=False, null=True, blank=True)
    is_curator = models.BooleanField(default=False, null=True, blank=True)
    email_subscribed = models.BooleanField(default=False, null=True, blank=True)
    def __str__(self):
        return self.user.username
