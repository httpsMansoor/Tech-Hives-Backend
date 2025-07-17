from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = [
    path('my_cart/', CartViewSet.as_view({'get': 'my_cart'})), 
    path('add_items/', CartViewSet.as_view({'post': 'add_items'})),
    path('remove_items/', CartViewSet.as_view({'post': 'remove_items'})),
    path('update_quantities/', CartViewSet.as_view({'put': 'update_quantities'})),
] + router.urls