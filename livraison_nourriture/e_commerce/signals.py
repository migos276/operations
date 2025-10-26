from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Restaurant_Plat, Menu
from users.models import Restaurant
from services.supabase_service import sync_table

@receiver(post_save, sender=Restaurant)
def sync_restaurant(sender, instance, **kwargs):
    sync_table("restaurants", {
        "id": str(instance.id),
        "nom": instance.nom,
        "logo":str(instance.logo),
        "rate": instance.rating,
        "rating_count": instance.rating_count,
        "rating_sum":instance.rating_sum,
    }, row_id=instance.id)

@receiver(post_save, sender=Restaurant_Plat)
def sync_plat(sender, instance, **kwargs):
    sync_table("plats", {
        "id": str(instance.id),
        "restaurant_id": str(instance.restaurant_id),
        "plat": instance.plat,
        "is_available": instance.is_available,
        "rating": instance.rating,
        "rating_count": instance.rating_count,
        "rating_sum":instance.rating_sum,
        "description": instance.description
    }, row_id=instance.id)

@receiver(post_save, sender=Menu)
def sync_menu_hebdo(sender, instance, **kwargs):
    sync_table("menu_hebdo", {
        "id": str(instance.id),
        "menu_hebdo_id": str(instance.menu_hebdo),
        "jour":str(instance.jour),
        "plats": [str(p.id) for p in instance.plats.all()],
    }, row_id=instance.id)

