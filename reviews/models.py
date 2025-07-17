from django.db import models
from django.conf import settings
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆ Poor'),
        (2, '★★☆☆☆ Fair'),
        (3, '★★★☆☆ Good'),
        (4, '★★★★☆ Very Good'),
        (5, '★★★★★ Excellent')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sentiment_score = models.FloatField(null=True, blank=True)  # For sentiment analysis
    
    class Meta:
        unique_together = ('user', 'product')  # One review per product per user
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating}★)"
    
    def save(self, *args, **kwargs):
        # Calculate sentiment score before saving
        self.sentiment_score = self.analyze_sentiment()
        super().save(*args, **kwargs)
        # Update product average rating
        self.product.update_rating()
        
    def analyze_sentiment(self):
        """Basic sentiment analysis (implement NLP logic here)"""
        positive_words = ['excellent', 'great', 'awesome', 'good', 'love']
        negative_words = ['poor', 'bad', 'terrible', 'awful', 'hate']
        
        if not self.comment:
            return None
            
        positive_count = sum(1 for word in positive_words if word in self.comment.lower())
        negative_count = sum(1 for word in negative_words if word in self.comment.lower())
        
        return (positive_count - negative_count) / len(self.comment.split()) if self.comment else 0