from rest_framework import serializers

from utility.models import GlobalSettings


class PublicWebsiteSerializer(serializers.ModelSerializer):
    logo_url = serializers.CharField(source='get_logo_url', read_only=True)

    class Meta:
        model = GlobalSettings
        fields = '__all__'
