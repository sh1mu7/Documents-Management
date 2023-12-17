from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('documents', views.ClientDocumentAPI)
router.register('profile', views.ClientProfileAPI)

urlpatterns = [

]

urlpatterns += router.urls
