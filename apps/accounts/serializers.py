from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from rest_framework import serializers
from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )

    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "password")

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number", ""),
            password=validated_data["password"],
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not authenticate(email=user.email, password=value):
            raise serializers.ValidationError(_("Old password is incorrect"))
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class ChangeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("phone_number",)

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number)
        instance.save()
        return instance


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        user = self.context["request"].user
        if CustomUser.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError(
                _("This email address is already in use"))
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.save()
        return instance
