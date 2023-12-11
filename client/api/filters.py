from django_filters import rest_framework as dj_filters

from client.models import Client


class AdminClientFilter(dj_filters.FilterSet):
    class Meta:
        model = Client
        fields = ('approval_status',)
