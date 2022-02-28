from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_page, name="login_page"),
    path('login/verify/', views.mobile_verify, name="mobile_verify"),
    path('login/changecode/', views.change_verify_code, name="change_verify_code"),

    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/profile/', views.profile, name="dashboard_profile"),
    path('dashboard/profile/<int:uid>/', views.profile, name="dashboard_user_profile"),
    path('dashboard/users/', views.users, name="dashboard_users"),
    path('dashboard/users/delete', views.users_delete, name="dashboard_users_delete"),

    path('dashboard/logout/', LogoutView.as_view(), name="dashboard_logout"),
]
