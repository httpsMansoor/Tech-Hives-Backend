from rest_framework import serializers
from .models import Review
from products.serializers import ProductSerializer

from rest_framework import serializers
from .models import Review
from products.serializers import ProductSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # This will show user's email or __str__ from CustomUser
    user_full_name = serializers.SerializerMethodField()
    product = ProductSerializer(read_only=True)
    sentiment = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id',
            'user',             # ← this line shows user __str__ (usually email)
            'user_full_name',   # ← this is full_name from your CustomUser model
            'product',
            'rating',
            'comment',
            'created_at',
            'sentiment_score',
            'sentiment'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'sentiment_score']

    def get_user_full_name(self, obj):
        return obj.user.full_name if obj.user.full_name else obj.user.email

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
