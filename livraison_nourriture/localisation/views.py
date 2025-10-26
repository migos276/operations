from django.shortcuts import render
# Create your views here.
from datetime import datetime
from django.utils import timezone
from rest_framework import viewsets,filters,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Produit
from users.models import CustomUser, Restaurant
from .models import Livraison, CommandeRestaurant, Commande_Plat
from .serializer import CommandeSerializer, LivraisonSerializer, CommandePlatSerializer


class CommadePlatViewSet(viewsets.ModelViewSet):
    queryset = Commande_Plat.objects.all()
    serializer_class = CommandePlatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['commande_id']
class CommandeRestaurantViewSet(viewsets.ModelViewSet):
    queryset = CommandeRestaurant.objects.all()
    serializer_class = CommandeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["commande_plat_set__plat_commander__menu__menu_hebdo__restaurant","commande_plat_set__plat_commander__plat","client__username"]
    filterset_fields = ['statut','jour','mois','annee']

    def destroy(self, request, *args, **kwargs):
        commande=self.get_object()
        if commande.statut!="attente":
            return Response({"detail":"Impossible de supprimer cette commande car elle a déjà été validé"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().destroy(request, *args, **kwargs)

class CommandeBoutiqueViewSet(viewsets.ModelViewSet):
    queryset = CommandeRestaurant.objects.all()
    serializer_class = CommandeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["commande_plat_set__produit__rayon__boutique","commande_plat_set__produit","client__username"]
    filterset_fields = ['statut','jour','mois','annee']
    def destroy(self, request, *args, **kwargs):
        commande=self.get_object()
        if commande.statut!="attente":
            return Response({"detail":"Impossible de supprimer cette commande car elle a déjà été validé"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().destroy(request, *args, **kwargs)


class LivraisonViewSet(viewsets.ModelViewSet):
    queryset = Livraison.objects.all()
    serializer_class = LivraisonSerializer

class RateCommande(APIView):
    def post(self,request):
        try:
            command_id=request.data.get("commande")
            commande=Commande_Plat.objects.get(id=command_id)
        except CommandeRestaurant.DoesNotExist:
            return Response({"error":"CommandeRestaurant not found "},status=status.HTTP_404_NOT_FOUND)
        rating=request.data.get("rating")
        if not rating:
            return Response({"error":"Rating is required"},status=status.HTTP_400_BAD_REQUEST)

        #-----mise à jour de la commande

        commande.rating_sum += float(rating)
        commande.rating_count+=1
        commande.rate=commande.rating_sum/commande.rating_count
        commande.save()

        #------mise à jour du plat

        plat=commande.plat_commander.plat
        plat.rating_sum += float(rating)
        plat.rating_count += 1
        plat.rate = plat.rating_sum / plat.rating_count
        plat.save()

        #-------mise à jour restaurant

        restaurant=plat.restaurant
        restaurant.rating_sum += float(rating)
        restaurant.rating_count += 1
        restaurant.rate = restaurant.rating_sum / restaurant.rating_count
        restaurant.save()

        return Response({
            "commande_rate":commande.rate,
            "plat_rate":plat.rate,
            "restaurant_rate":restaurant.rate
        }, status=status.HTTP_200_OK)


class RateLivreur(APIView):
    def post(self, request, livraison_id):
        try:
            livraison = Livraison.objects.get(id=livraison_id)
        except Livraison.DoesNotExist:
            return Response({"error": "livraison not found "}, status=status.HTTP_404_NOT_FOUND)
        rating = request.data.get("rating")
        if not rating:
            return Response({"error": "Rating is required"}, status=status.HTTP_400_BAD_REQUEST)

        # -----mise à jour de la commande
        livreur=livraison.livreur
        livreur.rating_sum += float(rating)
        livreur.rating_count += 1
        livreur.rate = livreur.rating_sum / livreur.rating_count
        livreur.save()

        return Response({
            "livreur_rate": livreur.rate,
        }, status=status.HTTP_200_OK)
class Update_Stock(APIView):
    def post(self,request):
        try:
            produit_id=request.data.get("produit")
            produit=Produit.objects.get(id=produit_id)
        except Produit.DoesNotExist:
            return Response({"error":"CommandeRestaurant not found "},status=status.HTTP_404_NOT_FOUND)
        quantite=request.data.get("quantite")
        if not quantite or int(quantite)<0:
            return Response({"error":"quantity is required"},status=status.HTTP_400_BAD_REQUEST)

        #-----mise à jour de la commande

        produit.quantite = int(quantite)
        produit.save()

        return Response({
            "produit_quantite":produit.quantite
        }, status=status.HTTP_200_OK)

class ClientCommande(APIView):
    def post(self, request):
        try:
            client_id = request.data.get("client")
            client = CustomUser.objects.get(id=client_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "user not found "}, status=status.HTTP_404_NOT_FOUND)
        commandes=client.commandes.all()
        data=[
            {
                "id":rp.id,
                "heure_de_commande": rp.heure_de_commande,
                "date": f"{rp.jour}/{rp.mois}/{rp.annee}",
                "prix_total": rp.prix_total,
                "restaurant":rp.commande_plat_set.plat_commander.menu.menu_hebdo.restaurant,
        }
            for rp in commandes

        ]

        return Response(data, status=status.HTTP_200_OK)
"""
class RestaurantCommande(APIView):
    def post(self, request, restaurant_id):
        try:
            restau = Restaurant.objects.get(id=restaurant_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "user not found "}, status=status.HTTP_404_NOT_FOUND)
        commandes=restau.menu_hebdo.menus.menu_plat_set.command_plat.commande.all()
        data=[
            {
                "id":rp.id,
                "heure_de_commande": rp.heure_de_commande,
                "date": f"{rp.jour}/{rp.mois}/{rp.annee}",
                "prix_total": rp.prix_total,
                "restaurant":rp.commande_plat_set.plat_commander.menu.menu_hebdo.restaurant,
        }
            for rp in commandes

        ]

        return Response(data, status=status.HTTP_200_OK)
"""