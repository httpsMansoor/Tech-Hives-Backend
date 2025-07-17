from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Order, ShippingAddress, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from cart.models import Cart, CartItem
import uuid
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

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
                return Response(
                    {'error': 'Your cart is empty'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check stock for all cart items before creating order
            for cart_item in cart.items.all():
                if cart_item.quantity > cart_item.product.stock:
                    return Response(
                        {'error': f'Not enough stock for {cart_item.product.name}. Requested: {cart_item.quantity}, Available: {cart_item.product.stock}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Create order
            payment_method = serializer.validated_data['payment_method']
            if payment_method == 'COD':
                payment_status = 'PENDING'
            else:
                # Simulate payment gateway success for now
                payment_status = 'PAID'
            order = Order.objects.create(
                user=request.user,
                order_number=str(uuid.uuid4())[:12].upper(),
                payment_method=payment_method,
                payment_status=payment_status,
                total_amount=cart.subtotal
            )

            # Create shipping address
            ShippingAddress.objects.create(
                order=order,
                **{k: v for k, v in serializer.validated_data.items() 
                   if k != 'payment_method'}
            )

            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Clear the cart
            cart.items.all().delete()

            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )

        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ConfirmOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            payment_method = order.payment_method
            if payment_method == 'COD':
                order.payment_status = 'PENDING'
            else:
                # Simulate payment gateway confirmation
                order.payment_status = 'PAID'
            # Only decrease stock if order is not already processing or beyond
            if order.status == 'PENDING':
                for item in order.items.all():
                    product = item.product
                    if product.stock >= item.quantity:
                        product.stock -= item.quantity
                        product.save()
                    else:
                        return Response({'error': f'Not enough stock for {product.name} to confirm order.'}, status=400)
                order.status = 'PROCESSING'
                order.save()
                return Response({'message': 'Order confirmed', 'order_status': order.status, 'payment_status': order.payment_status})
            else:
                return Response({'message': 'Order already confirmed or processed.', 'order_status': order.status, 'payment_status': order.payment_status})
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            if order.status not in ['PENDING', 'PROCESSING']:
                return Response({'error': 'Order cannot be cancelled at this stage.'}, status=400)
            # Restore stock for all order items
            for item in order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            order.status = 'CANCELLED'
            order.save()
            return Response({'message': 'Order cancelled and stock restored.', 'order_status': order.status})
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

class UserOrdersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')