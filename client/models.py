from django.db import models
from django.conf import settings
from client import constants
from coreapp.base import BaseModel


class DocumentType(BaseModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Client(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    required_documents = models.ManyToManyField(DocumentType, related_name='documents_types')
    approval_status = models.IntegerField(choices=constants.ApprovalStatus.choices,
                                          default=constants.ApprovalStatus.PENDING)

    def __str__(self):
        return self.user.get_full_name


class ClientDocument(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_documents')
    file = models.ForeignKey('coreapp.Document', on_delete=models.CASCADE, related_name='client_file')
    approval_status = models.IntegerField(choices=constants.ApprovalStatus.choices,
                                          default=constants.ApprovalStatus.PENDING)
    expiry_date = models.DateField(null=True)
    reject_reason = models.TextField(null=True)
    status = models.IntegerField(choices=constants.StatusType.choices, default=constants.StatusType.PENDING)

    def get_file_url(self):
        return self.file.get_url

    def __str__(self):
        return f'{self.client} - {self.file.get_url}'
