from rest_framework import serializers
from django.db import transaction
from users.models import Restaurant
from .models import Plat, Menu, Menu_Plat, MenuHebdomadaire, Restaurant_Plat, MenuStatique, MenuStatique_Plat


class PlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plat
        fields = ["nom"]

class RestaurantPlatSerializer(serializers.ModelSerializer):
    plat = PlatSerializer(read_only=True)
    plat_nom = serializers.CharField(write_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Restaurant_Plat
        fields = ['id',"plat","plat_nom", "restaurant","rate","is_avialable","image"]

    def create(self, validated_data):
        plat_nom = validated_data.pop("plat_nom")
        plat, _ = Plat.objects.get_or_create(nom=plat_nom)
        restaurant = validated_data.pop("restaurant")
        image = validated_data.get("image", None)

        if Restaurant_Plat.objects.filter(restaurant=restaurant, plat=plat).exists():
            raise serializers.ValidationError("Ce plat existe déjà pour ce restaurant")

        return Restaurant_Plat.objects.create(plat=plat, restaurant=restaurant, image=image)
class MenuPlatSerializer(serializers.ModelSerializer):
    plat = RestaurantPlatSerializer(read_only=True)
    plat_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant_Plat.objects.all(),
        write_only=True,
        source="plat"
    )

    class Meta:
        model = Menu_Plat
        fields = ['id',"plat", "plat_id", "prix","description","menu"]



class MenuSerializer(serializers.ModelSerializer):
    # source must point to the related_name or the default related manager
    plats = MenuPlatSerializer(source="menu_plat", many=True)

    class Meta:
        model = Menu
        fields = ["id", "plats", "jour", "menu_hebdo"]
        validators = [
            serializers.UniqueTogetherValidator(queryset=Menu.objects.all(), fields=['menu_hebdo', 'jour'],
                                                message="ce jour a déjà un menu")
        ]


    '''def update(self, instance, validated_data):
        plats_data = validated_data.pop("plats", [])

        if plats_data is not None:
            instance.menu_plat_set.all().delete()
            for plat_data in plats_data:
                Menu_Plat.objects.create(
                    menu=instance,
                    plat_id=plat_data["plat_id"],
                    prix=plat_data["prix"],
                    description=plat_data["description"]
                )
        return instance'''






class MenuHebdomadaireSerializer(serializers.ModelSerializer):
    menus=MenuSerializer(many=True, read_only=True)
    class Meta:
        model=MenuHebdomadaire
        fields=["id", "menus","restaurant"]

    @transaction.atomic
    def create(self, validated_data):
        menu_hebdo = super().create(validated_data)
        jours = [
            'lundi',
            'mardi',
            "mercredi",
            'jeudi',
            'vendredi',
            'samedi',
            'dimanche',
        ]
        for jour in jours:
            Menu.objects.create(menu_hebdo=menu_hebdo,jour=jour)
        return menu_hebdo
class CurrentMenuSerializer(serializers.ModelSerializer):
    # source must point to the related_name or the default related manager
    plat = RestaurantPlatSerializer(read_only=True)

    restaurant_id=serializers.IntegerField(source="menu.menu_hebdo.restaurant.id",read_only=True)
    restaurant = serializers.CharField(source="menu.menu_hebdo.restaurant.user.username", read_only=True)
    quartier = serializers.CharField(source="menu.menu_hebdo.restaurant.user.quartier", read_only=True)

    class Meta:
        model = Menu_Plat
        fields = ["id","plat", "prix","description","menu","restaurant_id","restaurant","quartier"]



class MenuStatiquePlatSerializer(serializers.ModelSerializer):
    plat = RestaurantPlatSerializer(read_only=True)
    plat_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant_Plat.objects.all(),
        write_only=True,
        source="plat"
    )
    menu = serializers.PrimaryKeyRelatedField(
        queryset=MenuStatique.objects.all(),
        write_only=True,
    )
    restaurant_id = serializers.IntegerField(source="menu.restaurant.id", read_only=True)
    restaurant = serializers.CharField(source="menu.restaurant.user.username", read_only=True)
    quartier = serializers.CharField(source="menu.restaurant.user.quartier", read_only=True)

    class Meta:
        model = MenuStatique_Plat
        fields = ['id',"plat", "plat_id", "prix","description","menu","restaurant_id","restaurant","quartier"]



class MenuStatiqueSerializer(serializers.ModelSerializer):
    plats = MenuStatiquePlatSerializer( many=True,read_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        write_only=True,
    )
    class Meta:
        model = MenuStatique
        fields = ["id", "plats","restaurant"]

#cree un menu
'''
post/data={
    menu_hebdo:menu_hebdo,
    jour:jour,
    menu_plat:{
        prix:prix,
        restau_plat:{
            
        

'''