from rest_framework import serializers
from .models import Review
from products.serializers import ProductSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = ProductSerializer(read_only=True)
    sentiment = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 
                 'created_at', 'sentiment_score', 'sentiment']
        read_only_fields = ['id', 'user', 'created_at', 'sentiment_score']
        
    def get_sentiment(self, obj):
        if obj.sentiment_score is None:
            return "neutral"
        return "positive" if obj.sentiment_score > 0 else "negative"
        
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment']
        
    def validate(self, data):
        user = self.context['request'].user
        if Review.objects.filter(user=user, product=data['product']).exists():
            raise serializers.ValidationError("You've already reviewed this product")
        return data