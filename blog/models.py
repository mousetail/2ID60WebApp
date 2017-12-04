from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    blog_content = models.TextField()
    blog_title = models.CharField(max_length=200)
    blog_published = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_published = models.DateTimeField()
    date_modified = models.DateTimeField()
