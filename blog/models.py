from django.db import models


# Create your models here.

class Blogs(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=256)
    body = models.TextField()
    image = models.ImageField(upload_to='blogs/')
    status = models.IntegerField(default=1)
    # visit = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
