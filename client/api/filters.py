from django_filters import rest_framework as dj_filters

from client.models import ClientDocument
from coreapp.models import User


class AdminClientFilter(dj_filters.FilterSet):
    class Meta:
        model = User
        fields = ('approval_status', 'id')


class ClientDocumentFilter(dj_filters.FilterSet):
    class Meta:
        model = ClientDocument
        fields = ('approval_status',)
