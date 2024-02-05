# Create your models here.
from django.utils import timezone
from django.db import models
from users.models import UserEx
from datetime import datetime as dt


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    picture = models.ImageField(upload_to='blog_pictures/')  
    publish_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
