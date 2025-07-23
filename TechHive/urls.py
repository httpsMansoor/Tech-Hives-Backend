from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API Documentation Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="TechHive API",
        default_version='v1',
        description="API documentation for TechHive - Smart Devices E-commerce Platform",
        terms_of_service="https://www.techhive.com/terms/",
        contact=openapi.Contact(email="contact@techhive.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[JWTAuthentication],
)

# API URL Patterns
api_urlpatterns = [
    path('auth/', include('userAuth.urls', namespace='accounts')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
     path('orders/', include('orders.urls')),
      path('reviews/', include('reviews.urls')),
    # Add other app URLs here as they are c
    # reated
]

# Documentation URL Patterns
docs_urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_superuser_view(request):
    User = get_user_model()
    
    email = "mansoorkhanabbaxi@gmail.com"
    password = "Nawankot@1"
    full_name = "Mansoor Khan"

    try:
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                full_name=full_name
            )
            return HttpResponse("✅ Superuser created successfully.")
        else:
            return HttpResponse("ℹ️ Superuser already exists.")
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}")

from django.core.management import call_command
from django.http import HttpResponse

def trigger_migration(request):
    call_command("makemigrations")
    call_command("migrate")
    return HttpResponse("Migrations completed.")





# Main URL Patterns
urlpatterns = [
    path("run-migrations/", trigger_migration),
    # Admin Interface
    path('admin/', admin.site.urls),
    path("create-superuser/", create_superuser_view),
    path('api/', include(api_urlpatterns)),
    
    # API Documentation
    path('', include(docs_urlpatterns)),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)