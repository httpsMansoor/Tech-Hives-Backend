from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product
from rest_framework.permissions import IsAuthenticated

class CartViewSet(viewsets.GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Retrieve the authenticated user's cart"""
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_items(self, request):
        """Add multiple items to the cart in one request"""
        items = request.data.get('items', [])
        cart, _ = Cart.objects.get_or_create(user=request.user)

        results = []
        for item in items:
            product_id = item.get('product')  # ✅ fixed key
            quantity = item.get('quantity', 1)

            try:
                product = Product.objects.get(id=product_id)
                if quantity > product.stock:
                    results.append({
                        'product_id': product_id,
                        'status': 'failed',
                        'error': f'Requested quantity ({quantity}) exceeds available stock ({product.stock})'
                    })
                    continue

                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': quantity}
                )

                if not created:
                    if cart_item.quantity + quantity > product.stock:
                        results.append({
                            'product_id': product_id,
                            'status': 'failed',
                            'error': f'Total quantity in cart ({cart_item.quantity + quantity}) exceeds available stock ({product.stock})'
                        })
                        continue
                    cart_item.quantity += quantity
                    cart_item.save()

                results.append({
                    'product_id': product_id,
                    'status': 'success',
                    'action': 'created' if created else 'updated'
                })
            except Product.DoesNotExist:
                results.append({
                    'product_id': product_id,
                    'status': 'failed',
                    'error': 'Product not found'
                })

        return Response({'results': results}, status=status.HTTP_207_MULTI_STATUS)

    @action(detail=False, methods=['post'])
    def remove_items(self, request):
        """Remove multiple items from cart"""
        item_ids = request.data.get('item_ids', [])
        deleted_count, _ = CartItem.objects.filter(
            id__in=item_ids,
            cart__user=request.user
        ).delete()

        return Response({
            'deleted_count': deleted_count,
            'remaining_items': request.user.cart.total_items
        })

    @action(detail=False, methods=['put'])
    def update_quantities(self, request):
        """Bulk update item quantities"""
        updates = request.data.get('updates', {})  # format: {item_id: quantity}

        updated_items = []
        for item_id, quantity in updates.items():
            try:
                item = CartItem.objects.get(id=item_id, cart__user=request.user)
                if quantity > item.product.stock:
                    updated_items.append({
                        'item_id': item_id,
                        'status': 'failed',
                        'error': f'Requested quantity ({quantity}) exceeds available stock ({item.product.stock})'
                    })
                    continue

                if quantity <= 0:
                    item.delete()
                    action = 'deleted'
                else:
                    item.quantity = quantity
                    item.save()
                    action = 'updated'

                updated_items.append({
                    'item_id': item_id,
                    'status': 'success',
                    'action': action
                })
            except CartItem.DoesNotExist:
                updated_items.append({
                    'item_id': item_id,
                    'status': 'failed',
                    'error': 'Item not found in your cart'
                })

        return Response({'results': updated_items})
