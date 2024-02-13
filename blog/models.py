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
    user = models.ForeignKey(UserEx,null=True,blank=True, on_delete=models.CASCADE)
    like_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(default=timezone.now)