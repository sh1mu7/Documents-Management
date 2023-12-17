from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.functional import cached_property
from client import constants as client_constant
from client.models import DocumentType
from coreapp import constants, roles
from coreapp.manager import MyUserManager
from .base import BaseModel


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ssn = models.CharField(unique=True, max_length=12)
    dob = models.DateField(null=True)
    image = models.ForeignKey('coreapp.Document', on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.SmallIntegerField(choices=constants.GenderChoices.choices, default=constants.GenderChoices.MALE)
    required_documents = models.ManyToManyField(DocumentType, related_name='documents_types', null=True)
    approval_status = models.IntegerField(choices=client_constant.ApprovalStatus.choices,
                                          default=client_constant.ApprovalStatus.PENDING, null=True)
    role = models.IntegerField(choices=roles.UserRoles.choices, default=roles.UserRoles.CLIENT)

    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @cached_property
    def get_image_url(self):
        return self.image.get_url if self.image_id else None


class UserConfirmation(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.confirmation_code} : {self.is_used}"


class LoginHistory(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=500)
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.ip_address} - {self.user_agent} - {self.is_success}"


class Document(BaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    doc_type = models.SmallIntegerField(choices=constants.DocumentChoices.choices)

    def __str__(self):
        return f"{self.owner} - {self.document.name}"

    @cached_property
    def get_url(self):
        return f"{settings.MEDIA_HOST}{self.document.url}"
