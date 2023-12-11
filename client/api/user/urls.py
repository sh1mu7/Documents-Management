from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('documents', views.ClientDocumentAPI)

urlpatterns = [

]

urlpatterns += router.urls
