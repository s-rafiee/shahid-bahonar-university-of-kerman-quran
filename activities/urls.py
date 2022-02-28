from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('dashboard/activities/', views.activities, name="dashboard_activities"),
    path('dashboard/activities/create_actual/', views.create_actual, name="dashboard_create_actual"),
    path('dashboard/activities/create_legal/', views.create_legal, name="dashboard_create_legal"),
    path('dashboard/activities/delete/', views.activities_delete, name="dashboard_activities_delete"),
    path('dashboard/activities/show/<int:aid>/', views.show_activitie, name="dashboard_show_activitie"),
    path('dashboard/activities/change/<int:aid>/', views.activitie_change_status, name="dashboard_activitie_change_status"),

    path('dashboard/activities/get_categories/', views.get_categories, name="dashboard_get_categories"),

    path('dashboard/categories/', views.categories, name="dashboard_categories"),
    path('dashboard/categories/<int:cid>/', views.categories, name="dashboard_categories"),
    path('dashboard/categories/delete/', views.categories_delete, name="dashboard_categories_delete"),
]
