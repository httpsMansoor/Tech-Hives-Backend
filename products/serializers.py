from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    parent = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        subs = obj.subcategories.all()
        return CategorySerializer(subs, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = (
            'average_rating',
            'review_count',
            'positive_reviews',
            'negative_reviews'
        )

    def get_image(self, obj):
        return obj.image.url if obj.image else None
