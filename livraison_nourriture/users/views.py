from django.shortcuts import render

from rest_framework import viewsets,filters,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Restaurant, Livreur, CustomUser, Boutique, HoraireHebdomadaire, Horaire
from users.serializer import RestaurantSerializer, LivreurSerializer, CustomUserSerializer, BoutiqueSerializer, \
    HoraireHebdoSerializer, HoraireSerializer, TypePlatSerializer
from users.utils import get_unique_code_for_model


# Create your views here.
def get_tokens_for_user(user):
    refresh=RefreshToken.for_user(user)
    access=refresh.access_token
    access['profile']=user.profile
    access['username'] = user.username
    return {
        'refresh':str(refresh),
        'access':str(access),
    }

class UserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['profile', 'email',"code"]


class RestaurantViewset(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    search_fields = ['user__username','user__email',"user__quartier"]
    filterset_fields = ['type_plat',"rate","est_ouvert","user"]



    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        restaurant=serializer.instance
        user=restaurant.user
        tokens=get_tokens_for_user(user)
        data=serializer.data
        data.update({
            'access':tokens['access'],
            'refresh': tokens["refresh"],
        })
        headers=self.get_success_headers(serializer.data)
        return Response(data,status=status.HTTP_201_CREATED,headers=headers)
class BoutiqueViewset(viewsets.ModelViewSet):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]

    search_fields = ['user__username',"user__quartier",'user__email']
    filterset_fields = ["est_ouvert","user"]

class LivreurViewset(viewsets.ModelViewSet):
    queryset = Livreur.objects.all()
    serializer_class = LivreurSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['entreprise',"user"]



from rest_framework.decorators import api_view
from services.supabase_service import sync_table

@api_view(["POST"])
def update_position(request):
    order_id = request.data.get("order_id")
    livreur_id = request.data.get("livreur_id")
    lat = request.data.get("latitude")
    lng = request.data.get("longitude")

    sync_table("delivery_positions", {
        "order_id": str(order_id),
        "livreur_id": livreur_id,
        "latitude": lat,
        "longitude": lng,
    })

    return Response({"status": "ok"})

@api_view(['POST'])
def create_entreprise(request):
    username = request.data.get("username")
    email = request.data.get("email")
    tel = request.data.get("tel")
    quartier = request.data.get("quartier")
    profile="entreprise"
    code=get_unique_code_for_model(CustomUser)

    entreprise=CustomUser.objects.create_user(username=username,email=email,tel=tel,quartier=quartier,profile=profile,password=code,code=code)

    return Response({"entreprise": entreprise}, status=200)

class HoraireHebdoViewset(viewsets.ModelViewSet):
    queryset = HoraireHebdomadaire.objects.all()
    serializer_class = HoraireHebdoSerializer

class HoraireViewset(viewsets.ModelViewSet):
    queryset = Horaire.objects.all()
    serializer_class = HoraireSerializer

class TypePlatListView(APIView):
    """
    Vue pour retourner tous les types de plats uniques
    """

    def get(self, request, *args, **kwargs):
        # On récupère tous les types de plats distincts
        types = Restaurant.objects.values_list('type_plat', flat=True).distinct()

        # On transforme en liste de dictionnaires pour serializer
        data = [{'type_plat': t} for t in types]

        serializer = TypePlatSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
