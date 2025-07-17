from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    average_rating = models.FloatField(default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    positive_reviews = models.PositiveIntegerField(default=0)
    negative_reviews = models.PositiveIntegerField(default=0)

    def update_rating(self):
        reviews = self.reviews.all()
        self.review_count = reviews.count()
        if self.review_count > 0:
            self.average_rating = sum(review.rating for review in reviews) / self.review_count
            self.positive_reviews = reviews.filter(sentiment_score__gt=0).count()
            self.negative_reviews = reviews.filter(sentiment_score__lt=0).count()
        else:
            self.average_rating = 0
            self.positive_reviews = 0
            self.negative_reviews = 0
        self.save()

    def __str__(self):
        return self.name
