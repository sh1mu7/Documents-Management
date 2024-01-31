from rest_framework import viewsets, mixins, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from client import constants
from client.models import ClientDocument
from coreapp.permissions import IsClientUser
from utility.api.public.serializers import PublicWebsiteSerializer
from utility.models import GlobalSettings


class PublicWebsiteAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [AllowAny, ]
    queryset = GlobalSettings.objects.all()
    serializer_class = PublicWebsiteSerializer


class UserDashboardInfo(views.APIView):
    permission_classes = [IsClientUser, ]

    def get(self, request):
        user = self.request.user
        total_files = ClientDocument.objects.filter(client=user).count()
        rejected_files = ClientDocument.objects.filter(client=user,
                                                       approval_status=constants.StatusType.REJECTED).count()
        pending_files = ClientDocument.objects.filter(client=user, approval_status=constants.StatusType.PENDING).count()
        approved_files = ClientDocument.objects.filter(client=user,
                                                       approval_status=constants.StatusType.APPROVED).count()

        response_data = {
            'total_files': total_files,
            'rejected_files': rejected_files,
            'pending_files': pending_files,
            'approved_files': approved_files,
        }

        return Response(response_data, status=status.HTTP_200_OK)
