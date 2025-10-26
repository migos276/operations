import datetime
from django.utils import timezone
from rest_framework import viewsets,filters,status,generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Restaurant
from .models import Menu, Plat, MenuHebdomadaire, Menu_Plat, MenuStatique, Restaurant_Plat, MenuStatique_Plat
from .serializer import MenuSerializer, PlatSerializer, MenuHebdomadaireSerializer, MenuPlatSerializer, \
    CurrentMenuSerializer, MenuStatiqueSerializer, RestaurantPlatSerializer, MenuStatiquePlatSerializer


class PlatViewSet(viewsets.ModelViewSet):
    queryset = Plat.objects.all()
    serializer_class = PlatSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields=["nom","id"]

class MenuPlatViewSet(viewsets.ModelViewSet):
    queryset = Menu_Plat.objects.all()
    serializer_class = MenuPlatSerializer

class MenuStatiquePlatViewSet(viewsets.ModelViewSet):
    queryset = MenuStatique_Plat.objects.all()
    serializer_class = MenuStatiquePlatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['plat__plat__nom', 'description']
    filterset_fields = ['prix', 'plat__rate']

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['plats__menu_plat__plat__nom']
    filterset_fields = ['jour']

class MenuHebdomadaireViewSet(viewsets.ModelViewSet):
    queryset = MenuHebdomadaire.objects.all()
    serializer_class = MenuHebdomadaireSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['menus__plats__plat__nom','menus__jour']
    filterset_fields = ['menus__jour', 'restaurant__id']
class CurrentMenuView(ListAPIView):
    serializer_class = CurrentMenuSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['plat__plat__nom','description']
    filterset_fields = ['menu']

    def get_queryset(self):
        jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
        today_index = timezone.localdate().weekday()  # plus sûr que datetime.today()
        today_str = jours[today_index]
        print("😁",today_str)
        return Menu_Plat.objects.filter(menu__jour=today_str)
class MenuStatiqueViewSet(viewsets.ModelViewSet):
    queryset = MenuStatique.objects.all()
    serializer_class = MenuStatiqueSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['restaurant__id']
    search_fields = ['plats__plat__nom','plats__description']



class RestaurantPlatViewSet(viewsets.ModelViewSet):
    queryset = Restaurant_Plat.objects.all()
    serializer_class = RestaurantPlatSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['restaurant__id','plat__id']
    search_fields = ['plat__nom']

class MesPlatsView(generics.ListAPIView):
    serializer_class = RestaurantPlatSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['plat__nom']

    def get_queryset(self):
        restaurant_id=self.kwargs.get('restaurant_id')
        return Restaurant_Plat.objects.filter(restaurant_id=restaurant_id)

class ClearMenuView(APIView):
    def delete(self,request,id):
        try:
            menu=Menu.objects.get(id=id)
            menu.menu_plat.all().delete()
            return Response({"message":"Tous les plats ont été supprimés"},status=status.HTTP_200_OK)
        except Menu.DoesNotExist:
            return Response({"error":"Menu introuvable."},status=status.HTTP_404_NOT_FOUND)

class ClearMenuStatiqueView(APIView):
    def delete(self,request,id):
        try:
            menu=MenuStatique.objects.get(id=id)
            menu.plats.all().delete()
            return Response({"message":"Tous les plats ont été supprimés"},status=status.HTTP_200_OK)
        except MenuStatique.DoesNotExist:
            return Response({"error":"Menu introuvable."},status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def plats_pas_cher_menu_du_jour(request):
    prix_max = request.data.get('prix_max', 200)
    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    today_index = timezone.localdate().weekday()  # plus sûr que datetime.today()
    today_str = jours[today_index]
    plats = Menu_Plat.objects.filter(
        prix__lte=prix_max,
        menu__jour=today_str
    ).distinct()

    serializer = MenuPlatSerializer(plats, many=True)
    return Response(serializer.data)



