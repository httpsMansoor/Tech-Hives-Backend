from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='review')

urlpatterns = [
    path('products/<int:product_id>/reviews/', 
         ReviewViewSet.as_view({'get': 'product_reviews'}), 
         name='product-reviews'),
] + router.urls