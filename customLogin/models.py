from django.db import models
from django.contrib.auth.models import AbstractUser
from customLogin.myusermanager import MyUserManager
from django_resized import ResizedImageField


# Create your models here.
class MyUser(AbstractUser):
    username = None
    password = None
    mobile = models.CharField(max_length=11, unique=True)
    national_code = models.CharField(max_length=10, unique=True)
    completed = models.BooleanField(default=False)
    gender = models.BooleanField(default=True)
    father = models.CharField(max_length=20)
    birthday = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    tel = models.CharField(max_length=11)
    image = ResizedImageField(upload_to='users/%Y/%m/%d/', quality=75, size=[300, 300], blank=True, null=True)

    otp = models.PositiveBigIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'mobile'

    REQUIRED_FIELDS = []

    backend = 'customLogin.mobilebackend.ModelBackend'
