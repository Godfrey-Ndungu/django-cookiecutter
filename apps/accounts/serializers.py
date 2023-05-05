from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[validate_password],
    )
    confirm_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "phone_number",
            "password",
            "confirm_password",
            "is_superuser",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data.get("phone_number", ""),
        )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password.
    """

    old_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )
    new_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[validate_password],
    )

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError("Incorrect password.")
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class ChangeProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for changing profile.
    """

    class Meta:
        model = CustomUser
        fields = ("phone_number",)

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get("phone_number",
                                                   instance.phone_number)
        instance.save()
        return instance


class ChangeEmailSerializer(serializers.Serializer):
    """
    Serializer for changing email.
    """

    email = serializers.EmailField()

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is already in use.")
        return email

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.save()
        return instance
