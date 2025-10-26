from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CommandeRestaurant
from services.supabase_service import sync_table

@receiver(post_save, sender=CommandeRestaurant)
def sync_order(sender, instance, **kwargs):
    sync_table("orders", {
        "id": str(instance.id),
        "client_id": instance.client_id,
        "restaurant_id": str(instance.restaurant_id),
        "status": instance.status,
    }, row_id=instance.id)
