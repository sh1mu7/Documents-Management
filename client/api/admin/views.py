from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, mixins
from django_filters import rest_framework as dj_filter
from rest_framework.decorators import action
from rest_framework.response import Response

from coreapp.models import User
from .. import filters
from ... import constants
from ...constants import ApprovalStatus, StatusType
from ...models import DocumentType, ClientDocument
from rest_framework.permissions import IsAdminUser, IsAdminUser
from .serializers import DocumentTypeSerializer, AdminClientSerializer, AdminClientApprovalStatusChangeSerializer, \
    AdminClientDocumentApprovalSerializer, AdminAddClientDocumentSerializer, AdminClientListSerializer


class AdminDocumentTypeAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = DocumentTypeSerializer
    queryset = DocumentType.objects.all()


class AdminClientAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = AdminClientSerializer
    queryset = User.objects.all()
    filter_backends = [dj_filter.DjangoFilterBackend]
    filterset_class = filters.AdminClientFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdminClientListSerializer
        return self.serializer_class

    @extend_schema(request=AdminClientApprovalStatusChangeSerializer)
    @action(detail=True, methods=['post'], url_path='client_status')
    def change_client_status(self, request, pk=None):
        client = self.get_object()
        serializer = AdminClientApprovalStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        approval_status = serializer.validated_data['approval_status']
        if not client.client_documents.filter(~Q(approval_status=ApprovalStatus.APPROVED)).exists():
            client.approval_status = ApprovalStatus.APPROVED
            client.save()
            return Response({'detail': "Client status changed successfully."}, status=status.HTTP_200_OK)
        client.approval_status = approval_status
        client.save()
        return Response({"Detail": "Not all documents are approved."},
                        status=status.HTTP_400_BAD_REQUEST)


class AdminClientDocumentsAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                              mixins.DestroyModelMixin):
    permission_classes = [IsAdminUser, ]
    serializer_class = AdminAddClientDocumentSerializer
    queryset = ClientDocument.objects.all()

    @extend_schema(request=AdminClientDocumentApprovalSerializer)
    @action(detail=True, methods=['post'], url_path='change_document_status')
    def change_document_status(self, request, pk=None):
        client_documents = self.get_object()
        serializer = AdminClientDocumentApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        approval_status = serializer.validated_data['approval_status']
        reject_reason = serializer.validated_data['reject_reason']

        if approval_status == ApprovalStatus.APPROVED:
            client_documents.approval_status = approval_status
            client_documents.status = StatusType.APPROVED
        elif approval_status == ApprovalStatus.REJECTED:
            client_documents.approval_status = approval_status
            client_documents.reject_reason = reject_reason
            client_documents.status = StatusType.REJECTED
        elif approval_status == ApprovalStatus.ON_PROCESSING:
            client_documents.approval_status = approval_status
            client_documents.status = StatusType.PENDING
        client_documents.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=None)
    @action(detail=False, methods=['get'], url_path='mark_all_approved/(?P<client_id>)')
    def mark_all_approve(self, request, client_id):
        client_documents = ClientDocument.objects.filter(client_id=client_id)

        for document in client_documents:
            document.approval_status = constants.ApprovalStatus.APPROVED
            document.status = constants.StatusType.APPROVED
            document.save()
        return Response({'detail': 'Success'}, status=status.HTTP_200_OK)
