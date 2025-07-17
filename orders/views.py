from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Order, ShippingAddress, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from cart.models import Cart, CartItem
import uuid
from drf_yasg.utils import swagger_auto_schema

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

            # Create order
            order = Order.objects.create(
                user=request.user,
                cart=cart,
                order_number=str(uuid.uuid4())[:12].upper(),
                payment_method=serializer.validated_data['payment_method'],
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