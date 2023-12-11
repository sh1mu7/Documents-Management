from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('document-type', views.AdminDocumentTypeAPI)
router.register('client', views.AdminClientAPI)
router.register('client-documents', views.AdminClientDocumentsAPI)

urlpatterns = [

]

urlpatterns += router.urls
