from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=500)
    writer = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_num = models.PositiveIntegerField(default=0)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post,blank=False, null=False, on_delete=models.CASCADE,related_name='comments')
    content = models.TextField(max_length=500)
    writer = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

