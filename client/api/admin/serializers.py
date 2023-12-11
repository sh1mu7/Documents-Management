from rest_framework import serializers

from coreapp.models import User
from ...models import DocumentType, Client, ClientDocument


class AdminAddClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'ssn')
        read_only_fields = ('email', 'ssn')


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'name', 'is_active')


class AdminClientDocumentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ClientDocument
        fields = ('id', 'client', 'file', 'approval_status', 'expiry_date', 'reject_reason', 'status')
        read_only_fields = ('reject_reason',)


class AdminClientSerializer(serializers.ModelSerializer):
    user = AdminAddClientSerializer(many=False, required=True)
    client_documents = AdminClientDocumentSerializer(many=True, required=True)

    class Meta:
        model = Client
        fields = '__all__'

    def create(self, validated_data):
        required_documents_data = validated_data.pop('required_documents')
        client_documents_data = validated_data.pop('client_documents')
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        client = Client.objects.create(**validated_data, user=user)
        client.required_documents.set(required_documents_data)
        for document_data in client_documents_data:
            ClientDocument.objects.create(client=client, **document_data)
        return client

    def update(self, instance, validated_data):
        user_data = validated_data['user']
        instance.user.__dict__.update(**user_data)
        password = user_data['password']
        instance.user.set_password(password)
        instance.user.save()
        instance.required_documents.set(validated_data['required_documents'])

        # Update or create client documents
        for doc_data in validated_data['client_documents']:
            doc_id = doc_data.pop('id', None)
            print(doc_id)
            if doc_id:
                client_doc = ClientDocument.objects.get(id=doc_id, client=instance)
                for key, value in doc_data.items():
                    setattr(client_doc, key, value)
                client_doc.save()
            else:
                ClientDocument.objects.create(client_id=instance.id, **doc_data)

        return instance


class AdminClientApprovalStatusChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('approval_status',)


class AdminClientDocumentApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDocument
        fields = ('approval_status', 'reject_reason')
