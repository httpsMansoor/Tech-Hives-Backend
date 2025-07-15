from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator, MinLengthValidator
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        help_text="Enter a secure password"
    )
    email = serializers.EmailField(
        help_text="Enter your email address",
        style={'placeholder': 'user@example.com'}
    )
    full_name = serializers.CharField(
        help_text="Enter your full name (letters and spaces only)",
        style={'placeholder': 'John Doe'},
        validators=[
            RegexValidator(
                regex='^[a-zA-Z\s]*$',
                message='Full name can only contain letters and spaces',
                code='invalid_full_name'
            ),
            MinLengthValidator(
                limit_value=3,
                message='Full name must be at least 3 characters long'
            )
        ],
        error_messages={
            'blank': 'Full name is required',
            'invalid': 'Full name can only contain letters and spaces'
        }
    )

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value.strip()).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'password']
        extra_kwargs = {
            'first_name': {'read_only': True, 'write_only': True},
            'last_name': {'read_only': True, 'write_only': True}
        }
        
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name']
        read_only_fields = ['id', 'email']