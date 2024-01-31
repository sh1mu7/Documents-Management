import os

from rest_framework import serializers

from coreapp.models import User
from ...models import ClientDocument, DocumentType


class ClientDocumentSerializer(serializers.ModelSerializer):
    document_type_name = serializers.CharField(source='get_document_title', read_only=True)
    file_url = serializers.CharField(source='get_file_url', read_only=True)

    class Meta:
        model = ClientDocument
        exclude = ('client',)


class UploadDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.CharField(source='file.get_url', read_only=True)

    class Meta:
        model = ClientDocument
        fields = ('file', 'file_url', 'document_type')

    def create(self, validated_data):
        user = self.context['request'].user
        client_documents = ClientDocument.objects.create(client=user, **validated_data)
        client_documents.save()
        return client_documents

    def validate(self, attrs):
        client = self.context['request'].user
        document_type = attrs.get('document_type')
        if client and document_type:
            if document_type not in client.required_documents.all():
                raise serializers.ValidationError("Document type is not valid")
        return attrs


class ClientProfileSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='get_image_url', read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'image', 'image_url', 'dob', 'gender', 'ssn', 'role', 'approval_status')
        read_only_fields = ('email', 'ssn', 'approval_status', 'role')


class ClientDocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'name',)
