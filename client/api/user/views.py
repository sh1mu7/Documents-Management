from rest_framework import viewsets, mixins
from ...models import ClientDocument
from .serializers import ClientDocumentSerializer
from rest_framework.permissions import IsAuthenticated


class ClientDocumentAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ClientDocumentSerializer
    queryset = ClientDocument.objects.all()

    def get_queryset(self):
        user = self.request.user
        return ClientDocument.objects.filter(client_id=user.id)
