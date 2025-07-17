from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer, CreateReviewSerializer
from products.models import Product
from rest_framework.decorators import action
from rest_framework.response import Response

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateReviewSerializer
        return ReviewSerializer
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['get'])
    def product_reviews(self, request, product_id=None):
        product = Product.objects.get(id=product_id)
        reviews = self.queryset.filter(product=product)
        serializer = self.get_serializer(reviews, many=True)
        return Response({
            'average_rating': product.average_rating,
            'total_reviews': product.review_count,
            'positive_reviews': product.positive_reviews,
            'negative_reviews': product.negative_reviews,
            'reviews': serializer.data
        })