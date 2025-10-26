from rest_framework_simplejwt.tokens import Token
from rest_framework import serializers
from .models import Rayon,Produit

class ProduitSerializer(serializers.ModelSerializer):

    class Meta:
        model=Produit
        fields=['id',"nom",'prix','unite',"quantite"]

class  RayonSerializer(serializers.ModelSerializer):
    produits=ProduitSerializer(read_only=True,many=True)

    class Meta:
        model=Rayon
        fields=['id',"nom",'boutique','produits']

