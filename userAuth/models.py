from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not full_name:
            raise ValueError('The Full Name field must be set')
        if not password:
            raise ValueError('Password is required')
            
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password, **extra_fields):
        # Set both flags to True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Validate the flags
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Create the superuser
        user = self.create_user(
            email=email,
            full_name=full_name,
            password=password,
            **extra_fields
        )
        
        # Ensure the flags are set
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        
        return user

class CustomUser(AbstractUser):
    username = None
    
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'A user with this email already exists.',
            'required': 'Email is required.',
            'blank': 'Email cannot be blank.'
        }
    )
    full_name = models.CharField(
        max_length=255,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r'^[a-zA-Z\s]*$',
                message='Name can only contain letters and spaces'
            )
        ],
        error_messages={
            'required': 'Full name is required.',
            'blank': 'Full name cannot be blank.'
        }
    )
    
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def clean(self):
        self.email = self.email.lower().strip()
        self.full_name = self.full_name.strip()
        super().clean()

    def __str__(self):
        return self.email
