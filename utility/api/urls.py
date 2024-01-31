from django.urls import include, path

urlpatterns = [
    path('admin/', include('utility.api.admin.urls')),
    path('mobile/', include('utility.api.public.urls'))

]

