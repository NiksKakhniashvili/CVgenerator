from rest_framework import serializers

from users.models import CustomUser
from utils.validation import emailvalidator


class CustomUserSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "first_name", "last_name")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
        Serializer class to serialize registration requests and create a new user.
    """
    email = serializers.EmailField(validators=[emailvalidator])

    class Meta:
        model = CustomUser
        fields = ("id", "email", "password", "username", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
