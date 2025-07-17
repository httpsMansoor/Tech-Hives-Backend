from django.urls import path
from .views import CheckoutView, ConfirmOrderView, UserOrdersView, CancelOrderView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('confirm/<int:order_id>/', ConfirmOrderView.as_view(), name='confirm-order'),
    path('my-orders/', UserOrdersView.as_view(), name='user-orders'),
    path('cancel/<int:order_id>/', CancelOrderView.as_view(), name='cancel-order'),
]