from rest_framework import serializers, status
from rest_framework.response import Response

from coreapp.models import User
from ...models import DocumentType, ClientDocument


class AdminAddClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'ssn')
        read_only_fields = ('email', 'ssn')


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'name', 'is_active')


class AdminAddClientDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.CharField(source='file.get_url', read_only=True)

    class Meta:
        model = ClientDocument
        fields = ('id', 'file', 'client', 'approval_status', 'expiry_date', 'reject_reason', 'status',
                  'file_url', 'document_type')
        read_only_fields = ('reject_reason',)

    def validate(self, attrs):
        client = attrs.get('client')
        document_type = attrs.get('document_type')
        if client and document_type:
            if document_type not in client.required_documents.all():
                raise serializers.ValidationError("Document type is not valid")
        return attrs


class AdminClientDocumentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    file_url = serializers.CharField(source='file.get_url', read_only=True)

    class Meta:
        model = ClientDocument
        fields = ('id', 'file', 'approval_status', 'expiry_date', 'reject_reason', 'status',
                  'file_url', 'document_type')
        read_only_fields = ('reject_reason',)


class AdminClientListSerializer(serializers.ModelSerializer):
    client_documents = AdminClientDocumentSerializer(many=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'ssn', 'client_documents', 'required_documents')


class AdminClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'ssn', 'required_documents')

    def create(self, validated_data):
        required_documents_data = validated_data.pop('required_documents')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data, is_verified=True, is_approved=True)
        user.set_password(password)
        user.save()
        user.required_documents.set(required_documents_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data['password']
        instance.set_password(password)
        instance.save()
        instance.required_documents.set(validated_data['required_documents'])
        return instance


class AdminClientApprovalStatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('approval_status',)


class AdminClientDocumentApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDocument
        fields = ('approval_status', 'reject_reason')
