from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'sentiment_score')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__email', 'comment')