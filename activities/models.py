from django.db import models
from customLogin.models import MyUser


# Create your models here.
class Categories(models.Model):
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=200, unique=True)
    parent = models.IntegerField(null=True, blank=True, default=0)
    type = models.IntegerField(null=False, blank=False)


class Activities(models.Model):
    cat = models.ForeignKey(Categories, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    person = models.IntegerField()
    exporter = models.CharField(max_length=200)
    start_date = models.DateField()
    expiration_date = models.DateField()
    company_name = models.CharField(max_length=200)
    admin_first_name = models.CharField(max_length=200)
    admin_last_name = models.CharField(max_length=200)
    admin_national_code = models.CharField(max_length=10)
    tel = models.CharField(max_length=11)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    image = models.ImageField(upload_to='activities/')
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
