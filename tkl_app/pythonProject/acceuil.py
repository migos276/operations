import datetime
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.metrics import dp
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import asyncio
from kivy.clock import Clock
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from api import userapi
from cards import ShopNearCard, FoodCard, ProductCard, RestauListItem
from tools import LoadPage, NoWifi,LimitedScrollView,LimitedRV

Window.size=(360,640)
Builder.load_file('acceuil.kv')



class Home(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        screen_manager = MDScreenManager()
        screen_manager.add_widget(MainHome(name="main-home"))
        screen_manager.add_widget(BoutiqueHome(name="boutique-home"))
        screen_manager.add_widget(RestaurantHome(name="restaurant-home"))
        screen_manager.transition = NoTransition()
        self.add_widget(screen_manager)

class RvCard(RecycleView):
    def __init__(self,**kwargs):
        super(RvCard, self).__init__(**kwargs)
        self.data=[]
    pass

class MainHome(MDScreen):
    nom="Kieran"
    username=f"Bonjour {nom.upper()}"
    location = "Bonamoussadi"

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def on_enter(self, *args):
        self.on_start()

    def on_start(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.start()))
    async def start(self):
        try:
            load=LoadPage()
            self.add_widget(load)
            self.ids['rv_near_shop'].clear_widgets()
            self.ids['rv_menu'].clear_widgets()
            self.ids['rv_product'].clear_widgets()


            shops=await userapi.rechercher_restaurant("logbessus")

            for shop in shops:
                self.ids['rv_near_shop'].add_widget(ShopNearCard(data=shop))

            # --- Restaurants ---
            restos = await userapi.rechercher_plat("")
            for resto in restos:
                print(resto)
                self.ids['rv_menu'].add_widget(FoodCard(data=resto))



            # --- Produits ---
            products = [
                {"nom":"Bouteille d’eau mineral 1L petryr",'image':"img/ndolé.jpg","boutique":"Carrefour market","quartier":"bonamoussadi","prix":"500 fcfa"},
                {"nom":"Bouteille d’eau mineral 1L",'image':"img/ndolé.jpg","boutique":"Carrefour market","quartier":"bonamoussadi","prix":"500 fcfa"},
            ]
            for product in products:
                self.ids['rv_product'].add_widget(ProductCard(data=product))

        except Exception as e:
            print(e)
            self.add_widget(NoWifi())

        finally:
            self.remove_widget(load)

class Tab(MDCard):
    text=StringProperty("")
    icon=StringProperty("")
    select=BooleanProperty(False)
    '''Class implementing content for a tab.'''



    def on_kv_post(self, base_widget):
        self.select_card()
    def select_card(self):

        if self.select:
            anim_card=Animation(md_bg_color=[217/255,217/255,217/255,1],duration=0.5,t="linear")
            print(self.ids)
            lab=self.ids["lab"]
            lab.bold=True
            anim_card.start(self)
        else:
            anim_card = Animation(md_bg_color=[0,0,0,0], duration=0.5, t="linear")
            lab = self.ids["lab"]
            anim_card.start(self)
            lab.bold = False

class RestaurantHome(MDScreen):
    nom = StringProperty(userapi.me["username"].upper())
    location = "Bonamoussadi"
    type_restau=StringProperty("tous")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tab_box=self.ids.tab_box
        self.on_start()

    def on_start(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.start()))
    def filter_type(self,type_text):
        if self.type_restau!=type_text:
            if type_text!="tous":
                Clock.schedule_once(lambda dt: asyncio.create_task(self.filter_type_restau_async(type=type_text)))
            else:
                Clock.schedule_once(lambda dt: asyncio.create_task(self.filter_type_restau_async()))

            for tab in self.tab_box.children:
                if tab.text== type_text:
                    pass
                else:
                    tab.select=False
                    tab.select_card()
            self.type_restau=type_text



    async def start(self):
        load = LoadPage()
        self.add_widget(load)

        try:
            # --- Restaurants proches ---
            print(1)
            shops = await userapi.rechercher_restaurant("logbessus")
            print(shops)
            self.ids.rv_near.clear_widgets()  # Toujours vider avant
            jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
            jour_actuel = jours[datetime.datetime.now().weekday()]

            for shop in shops:
                horaire_du_jour = next(
                    (h for h in shop["horaire"]["horaires"] if h["jour"].lower() == jour_actuel),
                    None
                )
                print("horairesssssss",horaire_du_jour)
                if horaire_du_jour:
                    heure_ouverture = datetime.datetime.strptime(horaire_du_jour['ouverture'], "%H:%M:%S").time()
                    heure_fermeture = datetime.datetime.strptime(horaire_du_jour['fermeture'], "%H:%M:%S").time()
                    maintenant = datetime.datetime.now().time()

                    if heure_ouverture <= maintenant <= heure_fermeture:
                        horaire = f"ferme à {horaire_du_jour['fermeture']}"
                    else:
                        horaire = f"ouvre à {horaire_du_jour['ouverture']}"
                else:
                    horaire = "Horaire non disponible"

                self.ids.rv_near.add_widget(ShopNearCard(data=shop, heure=horaire))

            # --- Tous les restaurants (RecycleView) ---
            print(2)
            types_plats=await userapi.recupérer_les_type_plat()
            for plat in types_plats:
                self.tab_box.add_widget(TabRestau(text=plat["type_plat"],main_parent=self))

            print(3)
            await self.filter_type_restau_async()
            print(4)

        except Exception as e:
            print(e)
            self.add_widget(NoWifi())

        finally:
            print(10)
            self.remove_widget(load)

    async def filter_type_restau_async(self,type=""):
        print(5)
        load=LoadPage()
        self.ids.rv_restau.parent.add_widget(load)
        try:
            print(6)
            restos = await userapi.filtre_restaurant(type_plat=type)
            # Vider la data avant de remplir
            print(7)
            self.ids.rv_restau.data = [{"viewclass": "RestauListItem", "data": resto} for resto in restos]
            print(8)
        except:
            self.add_widget(NoWifi())
        finally:
            self.ids.rv_restau.parent.remove_widget(load)




class TabRestau(MDCard):
    text=StringProperty("")
    select=BooleanProperty(False)
    main_parent=ObjectProperty()
    '''Class implementing content for a tab.'''



    def on_kv_post(self, base_widget):
        self.select_card()
    def select_card(self):

        if self.select:
            anim_card=Animation(md_bg_color=[169/255,4/255,4/255,1],duration=0.5,t="linear")
            print(self.ids)
            lab=self.ids["lab"]
            lab.bold=True
            anim_card.start(self)
            self.main_parent.filter_type(self.text.lower())
        else:
            anim_card = Animation(md_bg_color=[0,0,0,0], duration=0.5, t="linear")
            lab = self.ids["lab"]
            anim_card.start(self)
            lab.bold = False

class BoutiqueHome(MDScreen):
    nom=StringProperty(userapi.me["username"].upper())
    username=StringProperty(f"Bonjour {nom.get}")
    location = "Bonamoussadi"

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.on_start()

    def on_start(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.start()), 0.5)
    async def start(self):

        load=LoadPage()
        self.add_widget(load)
        try:
            shops=await userapi.rechercher_restaurant("logbessus")

            for shop in shops:
                jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
                jour_actuel = jours[datetime.datetime.now().weekday()]  # exemple: 'vendredi'

                # --- 2️⃣ Récupérer l’horaire correspondant ---
                horaire_du_jour = next(
                    (h for h in shop["horaire"]["horaires"] if h["jour"].lower() == jour_actuel),
                    None
                )
                heure_ouverture = datetime.datetime.strptime(horaire_du_jour['ouverture'], "%H:%M:%S").time()
                heure_fermeture = datetime.datetime.strptime(horaire_du_jour['fermeture'], "%H:%M:%S").time()

                # 2️⃣ Obtenir l'heure actuelle
                maintenant = datetime.datetime.now().time()

                # 3️⃣ Comparer
                if heure_ouverture <= maintenant <= heure_fermeture:
                    horaire = f"ferme à {horaire_du_jour['fermeture']}"
                else:
                    horaire = f"ouvre à {horaire_du_jour['ouverture']}"
                self.ids["rv_near_boutique"].add_widget(ShopNearCard(data=shop,heure=horaire ))

            # --- Restaurants ---
            restos = await userapi.rechercher_boutique("")
            print("restos",restos)
            self.ids.rv_boutique.data=[]
            self.ids.rv_boutique.data = [{"viewclass": "RestauListItem", "data": resto} for resto in restos]
        except Exception as e:
            print("❌❌",e)
            self.add_widget(NoWifi())

        finally:
            self.remove_widget(load)

class SearchPage(MDScreen):
    search_event=None
    def search(self,text):
        load=LoadPage()
        box = self.ids.main_box
        if self.search_event:
            self.search_event.cancel()
            box.remove_widget(load)
        box.add_widget(load)
        try:
            self.search_event=Clock.schedule_once(lambda dt:asyncio.create_task(self.search_async(text)),0.5)
        except:
            self.add_widget(NoWifi())
        finally:
            box.remove_widget(load)
    async def search_async(self,text):
        restaurant_box=self.ids.restau_box_search
        shop_box = self.ids.shop_box_search
        plat_box = self.ids.plat_box_search
        produit_box = self.ids.product_box_search
        restaurant_box.clear_widgets()
        shop_box.clear_widgets()
        plat_box.clear_widgets()
        produit_box.clear_widgets()

        if text:
            restau_data=await userapi.rechercher_restaurant(text)
            shop_data=await userapi.rechercher_boutique(text)
            plat_data=await  userapi.rechercher_plat(text)
            produit_data = await  userapi.rechercher_produit(text)



            n_restau=5 if len(restau_data)>=5 else len(restau_data)
            n_shop = 5 if len(shop_data) >= 5 else len(shop_data)
            n_plat = 10 if len(plat_data) >= 10 else len(plat_data)
            n_produit = 10 if len(produit_data) >= 10 else len(produit_data)

            for i in range(n_restau):
                restaurant_box.add_widget(RestauListItem(data=restau_data[i]))
            for i in range(n_shop):
                shop_box.add_widget(RestauListItem(data=shop_data[i]))
            for i in range(n_plat):
                plat_box.add_widget(FoodCard(data=plat_data[i],in_menu=True))
            for i in range(n_produit):
                produit_box.add_widget(ProductCard(data=produit_data[i]))


'''class App(MDApp):
    COLORS={
        "primary":"#A90404",
        "bg": "#ffffff",
        "light": "#D9D9D9",
        "normal": "#707070",
        "dark": "#1E1E1E",
    }
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style="Light"
        self.screen=SearchPage()
    def build(self):
        return self.screen

asyncio.run(App().async_run(async_lib='asyncio'))
'''