from rest_framework import serializers
from django.utils import timezone
from e_commerce.models import Menu_Plat
from e_commerce.serializer import PlatSerializer, MenuPlatSerializer
from users.models import Restaurant, CustomUser, Livreur
from users.serializer import CustomUserSerializer, RestaurantSerializer, LivreurSerializer
from .models import Position, CommandeRestaurant, Livraison, Commande_Plat


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["nom","latitude","longitude"]

class CommandePlatSerializer(serializers.ModelSerializer):
    plat_commander = serializers.PrimaryKeyRelatedField(queryset=Menu_Plat.objects.all(), write_only=True)
    plat = MenuPlatSerializer(read_only=True, source="plat_commander")
    class Meta:
        model=Commande_Plat
        fields=['id',"plat_commander","plat","quantite","prix_total","rate","commande"]

class CommandeSerializer(serializers.ModelSerializer):
    client_id=serializers.PrimaryKeyRelatedField( queryset=CustomUser.objects.all(),write_only=True,source="client")
    commande_plat_set=CommandePlatSerializer(many=True,write_only=True)
    plats=CommandePlatSerializer(many=True,read_only=True,source="commande_plat_set")
    client=CustomUserSerializer(read_only=True)
    restaurant=RestaurantSerializer(read_only=True,source="commande_plat_set__plat_commander__menu__menu_hebdo__restaurant")
    position=PositionSerializer()

    class Meta:
        model=CommandeRestaurant
        fields=['id',"client_id","client","plats","commande_plat_set","restaurant","position","prix_total","statut","heure_de_commande","jour","mois","annee"]

    def create(self, validated_data):
        print(validated_data)
        position_data=validated_data.pop("position")
        position=Position.objects.create(**position_data)
        print(validated_data)
        plats_data = validated_data.pop("commande_plat_set")
        today = timezone.localdate()
        validated_data["jour"]=today.day
        validated_data["mois"] = today.month
        validated_data["annee"] = today.year
        commande = CommandeRestaurant.objects.create(position=position, **validated_data)
        for plat_data in plats_data:
            Commande_Plat.objects.create(commande=commande, **plat_data)
        return commande

class LivraisonSerializer(serializers.ModelSerializer):
    livreur_id=serializers.PrimaryKeyRelatedField(queryset=Livreur.objects.all(), write_only=True,source="livreur")
    commande_id = serializers.PrimaryKeyRelatedField(queryset=CommandeRestaurant.objects.all(), write_only=True, source="commande")

    livreur=LivreurSerializer(read_only=True)
    commande=CommandeSerializer(read_only=True)

    class Meta:
        model=Livraison
        fields=['id',"livreur_id","livreur","commande_id","commande"]
