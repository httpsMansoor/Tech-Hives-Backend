import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# CORE DJANGO SETTINGS
# ======================
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-dev-only')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = ['*'] if DEBUG else os.getenv('ALLOWED_HOSTS', '').split(',')

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
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TechHive.urls'
WSGI_APPLICATION = 'TechHive.wsgi.application'
ASGI_APPLICATION = 'TechHive.asgi.application'

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

# ======================
# DATABASE CONFIGURATION
# ======================
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
# To switch to production DB:
# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.getenv('DATABASE_URL'),
#         conn_max_age=600,
#         ssl_require=not DEBUG
#     )
# }

# ======================
# PASSWORD VALIDATION
# ======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======================
# INTERNATIONALIZATION
# ======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================
# STATIC & MEDIA FILES
# ======================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Optional if you have extra static dirs
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ======================
# CUSTOM CONFIGURATIONS
# ======================
AUTH_USER_MODEL = 'userAuth.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================
# REST FRAMEWORK CONFIG
# ======================
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

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}

# ======================
# EMAIL CONFIGURATION
# ======================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', 10))
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ======================
# SECURITY CONFIGURATION
# ======================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# ======================
# CORS CONFIGURATION
# ======================
CORS_ALLOW_ALL_ORIGINS = DEBUG
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8081/",
        "https://yourapp.railway.app"
    ]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization',
    'content-type', 'dnt', 'origin', 'user-agent',
    'x-csrftoken', 'x-requested-with',
]

# ======================
# REST REGISTRATION
# ======================
REST_REGISTRATION = {
    'REGISTER_VERIFICATION_ENABLED': True,
    'REGISTER_EMAIL_VERIFICATION_ENABLED': True,
    'REGISTER_VERIFICATION_URL': os.getenv('REGISTER_VERIFICATION_URL', 'http://localhost:3000/verify-user/'),
    'REGISTER_EMAIL_VERIFICATION_URL': os.getenv('REGISTER_EMAIL_VERIFICATION_URL', 'http://localhost:3000/verify-email/'),
    'VERIFICATION_FROM_EMAIL': DEFAULT_FROM_EMAIL,
    'SEND_RESET_PASSWORD_LINK_SERIALIZER_USE_EMAIL': True,
    'RESET_PASSWORD_VERIFICATION_ENABLED': True,
    'RESET_PASSWORD_VERIFICATION_URL': os.getenv('RESET_PASSWORD_VERIFICATION_URL', 'http://localhost:8081/auth/reset-password/'),
    'RESET_PASSWORD_FAIL_WHEN_USER_NOT_FOUND': True,
    'LOGIN_SERIALIZER_CLASS': None,
    'REGISTER_SERIALIZER_CLASS': 'userAuth.serializers.UserRegistrationSerializer',
    'REGISTER_OUTPUT_SERIALIZER_CLASS': 'userAuth.serializers.UserProfileSerializer',
    'REGISTER_SERIALIZER_PASSWORD_CONFIRM': True,
    'USER_LOGIN_FIELDS': ['email'],
    'USER_HIDDEN_FIELDS': [
        'is_staff', 'is_superuser', 'is_active',
        'date_joined', 'last_login', 'groups',
        'user_permissions', 'first_name', 'last_name'
    ],
    'USER_EMAIL_FIELD': 'email',
    'VERIFICATION_EMAIL_BODY_HTML': '''
        <h3>Verify your account</h3>
        <p>Please click on the link below to verify your account:</p>
        <p><a href="{verification_url}">Verify Account</a></p>
        <p>The link will expire in 24 hours.</p>
    ''',
    'VERIFICATION_EMAIL_SUBJECT': 'Verify your TechHive account',
    'REGISTER_VERIFICATION_PERIOD': timedelta(days=1),
    'REGISTER_EMAIL_VERIFICATION_PERIOD': timedelta(days=1),
    'RESET_PASSWORD_VERIFICATION_PERIOD': timedelta(days=1),
}

# ======================
# SWAGGER CONFIGURATION
# ======================
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

# ======================
# OTP CONFIGURATION
# ======================
OTP_EXPIRY_TIME = int(os.getenv('OTP_EXPIRY_TIME', 10))  # minutes
