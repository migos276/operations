import datetime
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, DictProperty, NumericProperty, ListProperty
from kivy.metrics import dp
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelTwoLine
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import asyncio
from kivy.clock import Clock
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView

from api import img_url,userapi
from cards import ShopNearCard, FoodCard, ProductCard, RestauListItem
from tools import LoadPage, NoWifi,LimitedScrollView,LimitedRV

Window.size=(360,640)
Builder.load_file('restaurant.kv')

class RestaurantPage(MDScreen):
    data=DictProperty()
    md_bg_color = "#ffffff"
    heure= StringProperty()
    prev=ObjectProperty()
    image = StringProperty(img_url)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_restaurant()

    def on_enter(self, *args):
        self.get_restaurant()

    def get_restaurant(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.get_restaurant_async()))

    async def get_restaurant_async(self):
        print(self.data)
        if not self.data:
            print("entry")
            self.data= await userapi.avoir_restaurant(str(1))
        jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
        jour_actuel = jours[datetime.datetime.now().weekday()]

        horaire_du_jour = next(
            (h for h in self.data["horaire"]["horaires"] if h["jour"].lower() == jour_actuel),
            None
        )
        print("horairesssssss", horaire_du_jour)
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
        self.heure=horaire
        self.ids.meu_hebdo.data=self.data["menu_hebdo"] if self.data["menu_hebdo"] else []
        self.ids.menu_stat.data=self.data["menu_statique"] if self.data["menu_statique"] else []
        self.ids.meu_hebdo.on_start()
        self.ids.menu_stat.on_start()


    pass

class MenuHebdoPage(MDScreen):
    jours = {"lundi": {}, "mardi": {}, "mercredi": {}, "jeudi": {}, "vendredi": {}, "samedi": {}, "dimanche": {}}
    data=DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = MDBoxLayout(orientation="vertical", pos_hint={"center_x": 0.5, "top": 1}, adaptive_height=True)
        self.scrollview = LimitedScrollView()
        self.scrollview.add_widget(self.box)
        self.add_widget(self.scrollview)

    def on_enter(self, *args):
        self.on_start()

    def on_start(self):
        self.get_day()

    def get_day(self):
        load = LoadPage()
        self.add_widget(load)
        self.box.clear_widgets()
        for menu in self.data["menus"]:
            j = menu["jour"]
            self.jours[j] = menu
        print(self.jours)
        today_index = datetime.datetime.today().weekday()  # plus sûr que datetime.today()
        jours = list(self.jours.keys())
        print(jours)
        today_str=jours[today_index]
        today_elmt=ObjectProperty()
        for jour in self.jours.keys():
            if jour == today_str:
                element = MDExpansionPanel(
                        content=Content(data=self.jours[jour]["plats"],in_menu= True if jour==today_str else False ),
                        panel_cls=MDExpansionPanelTwoLine(
                            text="  "+jour,
                            secondary_text="  "+"aujourd'hui",
                            secondary_theme_text_color="Custom",
                            secondary_text_color="#A90404"

                        )
                    )
                today_elmt=element
            else:
                element = MDExpansionPanel(
                    content=Content(data=self.jours[jour]["plats"], in_menu=False),
                    panel_cls=MDExpansionPanelOneLine(
                        text="  " + jour

                    )
                )
            self.box.add_widget(element)
        today_elmt.open_panel(today_elmt.panel_cls)
        self.remove_widget(load)

class Content(MDBoxLayout):
    data=ListProperty()
    in_menu=BooleanProperty(False)

    def remplir(self):
        print(self.data)
        for resto in self.data:
            print(resto)
            self.add_widget(FoodCard(data=resto,size_hint_x=1,pos_hint={"center_x":.5},in_menu=self.in_menu))

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        print("mennnnnnnnnnu",self.data)
        self.adaptive_height=True
        self.padding=dp(10)
        self.spacing=dp(10)
        self.orientation="vertical"
        self.remplir()

class Menu_Statique(MDScreen):
    data = DictProperty()

    def on_start(self):
        self.ids.rv.data = [{"viewclass": "FoodCard", "data": resto} for resto in self.data]


'''
class App(MDApp):
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
        self.screen=RestaurantPage()
    def build(self):
        return self.screen

asyncio.run(App().async_run(async_lib='asyncio'))'''
