from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from coreapp.models import Document
from coreapp.utils import auth_utils, otp_utils

UserModel = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = (
            'email', 'ssn', 'first_name', 'last_name', 'dob', 'password', 'confirm_password',

        )

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': [_("Passwords do not match"), ]})
        return data

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password')
        user = UserModel.objects.create(**validated_data)
        user.set_password(confirm_password)
        user.is_approved = True
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs['email']
        try:
            user = auth_utils.get_user_by_email(email)
            auth_utils.validate_user(user)
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': [_(f"User with email {email} does not exist")]})


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        new_password = attrs['password']
        confirm_password = attrs['confirm_password']
        if new_password != confirm_password:
            raise serializers.ValidationError({'confirm_password': [_("Passwords do not match"), ]})
        auth_utils.validate_password(new_password)
        return attrs


class ForgetPassSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        try:
            user = auth_utils.get_user_by_email(email)
            auth_utils.validate_user(user)
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': [_(f"User with email {email} does not exist"), ]})


class ForgetPassConfirmSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']
        try:
            user = auth_utils.get_user_by_email(email)
            if not otp_utils.is_code_valid(user, code):
                raise serializers.ValidationError({'code': [_("Invalid code"), ]})
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': [_(f"User with email {email} does not exist"), ]})


class AccountVerifySerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']
        try:
            user = auth_utils.get_user_by_email(email)
            if not otp_utils.is_code_valid(user, code):
                raise serializers.ValidationError({'code': [_("Invalid code"), ]})
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': [_(f"User with email {email} does not exist"), ]})


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        try:
            user = auth_utils.get_user_by_email(email)
            auth_utils.validate_user(user)
            return attrs
        except ObjectDoesNotExist:
            raise serializers.ValidationError({'email': [_(f"User with email {email} does not exist"), ]})


class ProfileSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='get_image_url', read_only=True)

    class Meta:
        model = UserModel
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'ssn',
            'image',
            'image_url',
            'role'
        )
        read_only_fields = ('id', 'email', 'ssn', 'role')


class DocumentSerializer(serializers.ModelSerializer):
    doc_url = serializers.CharField(read_only=True, source="get_url")

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('owner',)
