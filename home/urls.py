from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homePage, name="home"),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('contactus/', views.contactus, name="contactus"),
    path('blogs/', views.blogs, name="blogs"),
    path('blog/<int:bid>/', views.blog, name="blog"),
    path('activists/<str:type>/', views.activists, name="activists"),
]
