from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CheckoutView, ConfirmOrderView, CancelOrderView,
    UserOrdersView, DeliveryAddressViewSet, PaymentMethodViewSet
)

router = DefaultRouter()
router.register('addresses', DeliveryAddressViewSet)
router.register('payments', PaymentMethodViewSet)

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('confirm/<int:order_id>/', ConfirmOrderView.as_view(), name='confirm_order'),
    path('cancel/<int:order_id>/', CancelOrderView.as_view(), name='cancel_order'),
    path('my/', UserOrdersView.as_view(), name='user_orders'),
    path('', include(router.urls)),
]
