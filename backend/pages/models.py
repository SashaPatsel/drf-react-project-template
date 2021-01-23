from django.db import models

class Tempfile(models.Model):
    uploaded = models.FileField(upload_to="temp/", null=True)