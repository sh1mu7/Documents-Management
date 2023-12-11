from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, mixins
from django_filters import rest_framework as dj_filter
from rest_framework.decorators import action
from rest_framework.response import Response
from .. import filters
from ... import constants
from ...models import DocumentType, Client, ClientDocument
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import DocumentTypeSerializer, AdminClientDocumentSerializer, AdminClientSerializer, \
    AdminClientApprovalStatusChangeSerializer, AdminClientDocumentApprovalSerializer


class AdminDocumentTypeAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()


class AdminClientAPI(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = AdminClientSerializer
    queryset = Client.objects.all()
    filter_backends = [dj_filter.DjangoFilterBackend]
    filterset_class = filters.AdminClientFilter

    @extend_schema(request=AdminClientApprovalStatusChangeSerializer)
    @action(detail=True, methods=['post'], url_path='client_status')
    def change_client_status(self, request, pk=None):
        client = self.get_object()
        serializer = AdminClientApprovalStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        approval_status = serializer.validated_data['approval_status']
        if not client.client_documents.filter(~Q(approval_status=constants.ApprovalStatus.APPROVED)).exists():
            client.approval_status = constants.ApprovalStatus.APPROVED
            client.save()
            return Response({'detail': "Client status changed successfully."}, status=status.HTTP_200_OK)
        client.approval_status = approval_status
        client.save()
        return Response({"Detail": "Not all documents are approved."},
                        status=status.HTTP_400_BAD_REQUEST)


class AdminClientDocumentsAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [AllowAny, ]
    serializer_class = AdminClientDocumentSerializer
    queryset = ClientDocument.objects.all()

    # @extend_schema(request=AdminClientDocumentApprovalSerializer)
    # @action(detail=True, methods=['post'], url_path='client_document_status')
    # def change_client_document_status(self, request, pk=None):
    #     client_documents = self.get_object()
    #     serializer = AdminClientDocumentApprovalSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     approval_status = serializer.validated_data['approval_status']
    #     reject_reason = serializer.validated_data['reject_reason']
    #     if client_documents.approval_status == constants.ApprovalStatus.APPROVED:
    #         client_documents.status = constants.StatusType.APPROVE
    #     elif client_documents.approval_status == constants.ApprovalStatus.REJECTED:
    #         client_documents.reject_reason = reject_reason
    #         client_documents.status = constants.StatusType.REJECT
