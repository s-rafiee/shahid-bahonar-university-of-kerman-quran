from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/blogs/', views.blogs, name="dashboard_blogs"),
    path('dashboard/blogs/create/', views.create_blog, name="dashboard_create_blogs"),
    path('dashboard/blogs/edit/<int:bid>/', views.create_blog, name="dashboard_edit_blogs"),
    path('dashboard/blogs/delete/', views.delete_blogs, name="dashboard_delete_blogs"),
    path('dashboard/blogs/change_status/', views.change_status_blogs, name="dashboard_change_status_blogs"),
]
