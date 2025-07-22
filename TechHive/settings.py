

from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_xs9gv!yagk=47tvguanq8w$#^r%p=^wy954nr28336$)ub2@&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.221.253.88','responding-dig-spent-virginia.trycloudflare.com', '.ngrok-free.app']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_registration',
    'drf_yasg',
    'django_filters',
    'corsheaders',
    
    # Local apps
    'userAuth',
    'products',
    'cart',
    'orders',
    'reviews',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TechHive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TechHive.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'techhive',
        'USER': 'admin',
        'PASSWORD': 'admin123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'userAuth.CustomUser'

# REST Framework settings   
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_TIMEOUT = 10  # Reduced timeout to 10 seconds
EMAIL_USE_SSL = False
EMAIL_SSL_CERTVERIFY = True
EMAIL_CONNECTION_TIMEOUT = 5  # Reduced connection timeout to 5 seconds
EMAIL_READ_TIMEOUT = 5  # Reduced read timeout to 5 seconds

# Additional SMTP settings
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# OTP Configuration
OTP_EXPIRY_TIME = 10  # OTP validity in minutes

# Update REST_REGISTRATION settings
REST_REGISTRATION = {
    'REGISTER_VERIFICATION_ENABLED': True,  # Enable verification
    'REGISTER_EMAIL_VERIFICATION_ENABLED': True,  # Enable email verification
    'REGISTER_VERIFICATION_URL': 'http://localhost:3000/verify-user/',  # Frontend verification URL
    'REGISTER_EMAIL_VERIFICATION_URL': 'http://localhost:3000/verify-email/',  # Added this line
    'VERIFICATION_FROM_EMAIL': os.getenv('EMAIL_HOST_USER', 'noreply@techhive.com'),
    'SEND_RESET_PASSWORD_LINK_SERIALIZER_USE_EMAIL': True,
    'RESET_PASSWORD_VERIFICATION_ENABLED': True,
    'RESET_PASSWORD_VERIFICATION_URL': 'http://localhost:8081/auth/reset-password/',
    'RESET_PASSWORD_FAIL_WHEN_USER_NOT_FOUND': True,
    'LOGIN_SERIALIZER_CLASS': None,
    'REGISTER_SERIALIZER_CLASS': 'userAuth.serializers.UserRegistrationSerializer',
    'REGISTER_OUTPUT_SERIALIZER_CLASS': 'userAuth.serializers.UserProfileSerializer',  # Added this line
    'REGISTER_SERIALIZER_PASSWORD_CONFIRM': True,  # Enable password confirmation
    'USER_LOGIN_FIELDS': ['email'],
    'USER_HIDDEN_FIELDS': ['is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login', 'groups', 'user_permissions', 'first_name', 'last_name'],  # Added first_name and last_name
    'USER_EMAIL_FIELD': 'email',
    'VERIFICATION_EMAIL_BODY_HTML': '''
        <h3>Verify your account</h3>
        <p>Please click on the link below to verify your account:</p>
        <p><a href="{verification_url}">Verify Account</a></p>
        <p>The link will expire in 24 hours.</p>
    ''',
    'VERIFICATION_EMAIL_SUBJECT': 'Verify your TechHive account',
    'REGISTER_VERIFICATION_PERIOD': timedelta(days=1),  # Verification link expires in 1 day
    'REGISTER_EMAIL_VERIFICATION_PERIOD': timedelta(days=1),
    'RESET_PASSWORD_VERIFICATION_PERIOD': timedelta(days=1),
}

# Swagger settings
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer your_token_here"',
        }
    },
    'USE_SESSION_AUTH': False,
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Only for development
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Security settings for HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
