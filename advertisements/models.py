from django.db import models
from users.models import User

# Create your models here.

class Advertisements(models.Model):
    ad_name = models.CharField(max_length=255)
    ad_title = models.CharField(max_length=255)
    ad_desc = models.CharField(max_length=255)
    creator = models.IntegerField(null=True)
    is_published = models.BooleanField(default=False)

    REQUIRED_FIELDS = []