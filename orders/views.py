from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, DeliveryAddress, PaymentMethod
from .serializers import (
    OrderSerializer, OrderItemSerializer, CheckoutSerializer,
    DeliveryAddressSerializer, PaymentMethodSerializer
)
from cart.models import Cart
from drf_yasg.utils import swagger_auto_schema
import uuid

# ----------------------------
# 📦 Checkout Order
# ----------------------------

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CheckoutSerializer)
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(user=request.user)
            if not cart.items.exists():
                return Response({'error': 'Your cart is empty'}, status=400)

            # Validate address & payment
            address_id = serializer.validated_data['delivery_address_id']
            payment_id = serializer.validated_data['payment_method_id']
            try:
                address = DeliveryAddress.objects.get(id=address_id, user=request.user)
                payment = PaymentMethod.objects.get(id=payment_id, user=request.user)
            except (DeliveryAddress.DoesNotExist, PaymentMethod.DoesNotExist):
                return Response({'error': 'Invalid address or payment method'}, status=404)

            # Stock check
            for item in cart.items.all():
                if item.quantity > item.product.stock:
                    return Response({
                        'error': f'Not enough stock for {item.product.name}. Requested: {item.quantity}, Available: {item.product.stock}'
                    }, status=400)

            # Create order
            order = Order.objects.create(
                user=request.user,
                order_number=str(uuid.uuid4())[:12].upper(),
                delivery_address=address,
                payment_method=payment,
                payment_status='PENDING' if payment.method_type == 'COD' else 'PAID',
                total_amount=cart.subtotal
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Empty cart
            cart.items.all().delete()

            return Response(OrderSerializer(order).data, status=201)

        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)

# ----------------------------
# ✅ Confirm Order
# ----------------------------

class ConfirmOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)

            if order.status != 'PENDING':
                return Response({'message': 'Order already confirmed or processed.'})

            if order.payment_method.method_type != 'COD':
                order.payment_status = 'PAID'

            for item in order.items.all():
                product = item.product
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                    product.save()
                else:
                    return Response({'error': f'Not enough stock for {product.name} to confirm order.'}, status=400)

            order.status = 'PROCESSING'
            order.save()

            return Response({
                'message': 'Order confirmed',
                'order_status': order.status,
                'payment_status': order.payment_status
            })

        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

# ----------------------------
# ❌ Cancel Order
# ----------------------------

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            if order.status not in ['PENDING', 'PROCESSING']:
                return Response({'error': 'Order cannot be cancelled at this stage.'}, status=400)

            for item in order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()

            order.status = 'CANCELLED'
            order.save()

            return Response({'message': 'Order cancelled and stock restored.', 'order_status': order.status})
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

# ----------------------------
# 📄 List User Orders
# ----------------------------

class UserOrdersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

# ----------------------------
# 📍 Address Management
# ----------------------------

class DeliveryAddressViewSet(viewsets.ModelViewSet):
    queryset = DeliveryAddress.objects.all()  # Required for DRF router
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ----------------------------
# 💳 Payment Method Management
# ----------------------------

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()  # Required for DRF router
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
