from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review

@receiver([post_save, post_delete], sender=Review)
def update_product_rating(sender, instance, **kwargs):
    instance.product.update_rating()