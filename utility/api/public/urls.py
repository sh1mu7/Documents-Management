from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('global_settings', views.PublicWebsiteAPI)

urlpatterns = [
    path('user-dashboard-info/', views.UserDashboardInfo.as_view())
]
urlpatterns += router.urls
