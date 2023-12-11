from rest_framework import serializers
from ...models import ClientDocument


class ClientDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.CharField(source='get_file_url', read_only=True)

    class Meta:
        model = ClientDocument
        fields = '__all__'
