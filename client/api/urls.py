from django.urls import path, include

urlpatterns = [
    path('admin/', include('client.api.admin.urls')),
    path('client/', include('client.api.user.urls')),
]
