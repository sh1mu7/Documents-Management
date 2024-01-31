from django.urls import path
from . import views



urlpatterns = [
    path('site-info/', views.GlobalSettingsAPI.as_view()),
    path('dashboard-info/', views.DashboardInfo.as_view())
]

