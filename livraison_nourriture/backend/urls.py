"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include

from e_commerce.views import PlatViewSet, MenuHebdomadaireViewSet, MenuViewSet, CurrentMenuView, RestaurantPlatViewSet, \
    MenuStatiqueViewSet, MenuPlatViewSet, MesPlatsView, ClearMenuView, MenuStatiquePlatViewSet, ClearMenuStatiqueView, \
    plats_pas_cher_menu_du_jour
from payement.views import CollectMoneyView, DepositMoneyView
from shop.views import ProduitViewset, RayonViewset
from users.views import RestaurantViewset, HoraireHebdoViewset, UserViewset, LivreurViewset, BoutiqueViewset, \
    create_entreprise, HoraireViewset, TypePlatListView
from localisation.views import CommandeRestaurantViewSet, LivraisonViewSet, RateCommande, CommadePlatViewSet, \
    CommandeBoutiqueViewSet, Update_Stock
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenBlacklistView
#from payement.views import initier_paiement, webhook_pawapay, retirer_argent

routeur=DefaultRouter()
routeur.register(r'plat',PlatViewSet)
routeur.register(r'menu_plat',MenuPlatViewSet)
routeur.register(r'menu_static_plat',MenuStatiquePlatViewSet)
routeur.register(r'menu',MenuViewSet,basename="menu")
routeur.register(r'menu_hebdo',MenuHebdomadaireViewSet)
routeur.register(r'menu_statique',MenuStatiqueViewSet)
routeur.register(r'restaurant_plat',RestaurantPlatViewSet)
routeur.register(r'restaurant',RestaurantViewset,basename="restaurant")
routeur.register(r'livreur',LivreurViewset)
routeur.register(r'utilisateur',UserViewset)
routeur.register(r'livraison',LivraisonViewSet)
routeur.register(r'commande_restau', CommandeRestaurantViewSet, basename="commandeRestaurant")
routeur.register(r'commande_plat',CommadePlatViewSet)
routeur.register(r'commande_boutique', CommandeBoutiqueViewSet, basename="commandeBoutique")
routeur.register(r'produit',ProduitViewset)
routeur.register(r'boutique',BoutiqueViewset)
routeur.register(r'rayons',RayonViewset)
routeur.register(r'horaire',HoraireViewset)
routeur.register(r'horaire_hebdomadaire',HoraireHebdoViewset)

urlpatterns = [
    path('', include(routeur.urls)),
    path('admin/', admin.site.urls),
    path('today/', CurrentMenuView.as_view(),name="menu-current"),
    path("token/",TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("logout/",TokenBlacklistView.as_view(),name="logout"),
    path("commande/plats/rate/",RateCommande.as_view(),name="rate-plats"),
    path("produit/update",Update_Stock.as_view(),name="update-stock"),
    path("livraisons/livreur/<int:commande_id>/rate/",RateCommande.as_view(),name="rate-plats"),
    path("payement/send/", CollectMoneyView.as_view(), name="collect"),
    path("payement/receive/", DepositMoneyView.as_view(), name="deposit"),
    #path("payement/rerait/", retirer_argent, name="deposit"),
    path('plats/pas_cher/', plats_pas_cher_menu_du_jour),
    path("restaurants/new/",create_entreprise,name="new entreprise"),
    path("restaurant/<int:restaurant_id>/plats/",MesPlatsView.as_view(),name="plats-du-restau"),
    path("menu/<int:id>/clear/",ClearMenuView.as_view(),name="vider-le-menu"),
    path('types-plats/', TypePlatListView.as_view(), name='types_plats'),
    path("menu_statique/<int:id>/clear/", ClearMenuStatiqueView.as_view(), name="vider-le-menu-statique")

]
