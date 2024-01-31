from django.db.models import Sum
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import viewsets, mixins, views, status
from rest_framework.permissions import AllowAny, IsAdminUser

from coreapp.models import User
from . import serializers
from ...models import GlobalSettings


class GlobalSettingsAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    @extend_schema(
        responses={200: serializers.GlobalSettingsSerializer}
    )
    def get(self, request):
        global_settings = GlobalSettings.objects.first()
        serializer = serializers.GlobalSettingsSerializer(global_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: serializers.GlobalSettingsSerializer},
        request=serializers.GlobalSettingsSerializer
    )
    def post(self, request):
        global_settings = GlobalSettings.objects.first()
        serializer = serializers.GlobalSettingsSerializer(data=request.data, instance=global_settings)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DashboardInfo(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        total_clients = User.objects.filter(role=1).count()
        total_pending = User.objects.filter(approval_status=0, role=1).count()
        total_approved = User.objects.filter(approval_status=1, role=1).count()
        total_on_processing = User.objects.filter(approval_status=2, role=1).count()
        total_rejected = User.objects.filter(approval_status=3, role=1).count()

        data = {
            'total_clients': total_clients,
            'total_pending': total_pending,
            'total_approved': total_approved,
            'total_on_processing': total_on_processing,
            'total_rejected': total_rejected

        }
        return Response(data, status=status.HTTP_200_OK)
