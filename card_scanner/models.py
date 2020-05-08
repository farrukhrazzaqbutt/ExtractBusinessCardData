from django.db import models

# Create your models here.
class ScanCard(models.Model):
    id = models.AutoField(auto_created=True,primary_key=True)
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='UploadImages/%Y/%m/%d/', max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)