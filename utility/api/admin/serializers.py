from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ...models import GlobalSettings


class GlobalSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.CharField(source='get_logo_url', read_only=True)

    class Meta:
        model = GlobalSettings
        fields = '__all__'
