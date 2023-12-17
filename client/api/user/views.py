from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from django_filters import rest_framework as dj_filter
from rest_framework.decorators import action
from rest_framework.response import Response

from coreapp.models import User
from coreapp.permissions import IsClientUser
from .. import filters
from ...models import ClientDocument
from .serializers import ClientDocumentSerializer, ClientProfileSerializer, UploadDocumentSerializer, \
    ClientDocumentTypeSerializer
from rest_framework.permissions import IsAuthenticated


class ClientDocumentAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsClientUser, ]
    serializer_class = ClientDocumentSerializer
    queryset = ClientDocument.objects.all()
    filter_backends = [dj_filter.DjangoFilterBackend]
    filterset_class = filters.ClientDocumentFilter

    def get_queryset(self):
        user = self.request.user
        return ClientDocument.objects.filter(client_id=user.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return UploadDocumentSerializer
        return self.serializer_class


class ClientProfileAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    permission_classes = [IsClientUser, ]
    serializer_class = ClientProfileSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)

    @extend_schema(responses=ClientDocumentTypeSerializer)
    @action(detail=False, methods=['get'], url_path='client-document-type')
    def get_client_document_type(self, request, *args, **kwargs):
        client = self.request.user
        required_documents = client.required_documents.all()
        serializer = ClientDocumentTypeSerializer(required_documents, many=True)
        return Response(serializer.data)
