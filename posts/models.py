from distutils.command.upload import upload
from os import supports_bytes_environ
from pyexpat import model
from statistics import mode
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , related_name='user_post' , on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/image/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    edit = models.BooleanField(default=False)
    edit_time = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True , max_length=300)
    user_likes = models.ManyToManyField(settings.AUTH_USER_MODEL , related_name='posts_like' , blank=True)
    
    def __str__(self):
        return str(self.user)+str(datetime.now())
    
    def save(self , *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.user)+str(datetime.now()))
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("posts:detail_post", kwargs={"id": self.id , "slug":self.slug})



        
class PostComment(models.Model):
    post = models.ForeignKey(Post , related_name='comment_post' , on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL , related_name='comment_user' , on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edit = models.BooleanField(default=False)
    edit_time = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL , related_name='comment_like' , blank=True)
    
    def __str__(self):
        return f'{self.post.id} {self.user}'
    
    