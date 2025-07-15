from django.urls import path
from rest_registration.api.views import (
    register, 
    send_reset_password_link, 
    reset_password,
    verify_registration,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'accounts'

urlpatterns = [
    # Registration and verification
    path('register/', register, name='register'),
    path('verify-registration/', verify_registration, name='verify-registration'),
    
    # Password reset
    path('send-reset-password-link/', send_reset_password_link, name='send-reset-password-link'),
    path('reset-password/', reset_password, name='reset-password'),
    
    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]