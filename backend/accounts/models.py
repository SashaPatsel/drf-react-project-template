from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Permissions(models.Model):
    rrm = models.CharField(max_length=40)
    # Sorted by for admin
    def __str__(self):
        return self.rrm

class Account(models.Model):
    # id = models.BigIntegerField(primary_key = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)
    regulator = models.BooleanField(default=False, null=True, blank=True)
    expert_badge = models.BooleanField(default=False, null=True, blank=True)
    is_curator = models.BooleanField(default=False, null=True, blank=True)
    email_subscribed = models.BooleanField(default=False, null=True, blank=True)
    # helpers loop through five default images
    # Sorted by for admin
    def __str__(self):
        return self.user.username

class Curator(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    accepted = models.BooleanField(default=False)

class Species_Expert(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    species = models.CharField(max_length=200)
    species_colloquial = models.CharField(max_length=200, null=True, blank=True)
    tax_class = models.CharField(max_length=200, null=True, blank=True)
    organization = models.CharField(max_length=200, null=True, blank=True)
    info_and_links = models.TextField(null=True, blank=True)
    badge_pending = models.BooleanField(default=True, null=True, blank=True)
    was_endorsed = models.BooleanField(default=False, null=True, blank=True)
    recommended_rejection = models.BooleanField(default=False, null=True, blank=True)
    recommended_removal = models.BooleanField(default=False, null=True, blank=True)

class Whitelist(models.Model):
    email = models.CharField(max_length=201)
    full_name = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.email

class File(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    data = models.FileField(upload_to="files/%Y/%m/%d/")
    upload_date = models.DateTimeField(default=datetime.now, blank=True)
    title = models.CharField(max_length=100)

class Notification(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE,  related_name='account_notified')
    message = models.CharField(max_length=800, null=True, blank=True)
    link = models.CharField(max_length=800, null=True, blank=True)
    app = models.CharField(max_length=100, null=True, blank=True)
    content_id = models.IntegerField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now, blank=True)   

class Feedback(models.Model):
    fb_text = models.TextField()
    resolved = models.BooleanField(default=False)
    name = models.CharField(max_length=800, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
