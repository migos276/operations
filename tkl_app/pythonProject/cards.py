from kivy.animation import Animation
from kivy.properties import ObjectProperty, StringProperty, DictProperty, BooleanProperty, NumericProperty
from kivymd.app import MDApp
import asyncio
import httpx
from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import ThreeLineAvatarIconListItem
from kivymd.uix.snackbar import MDSnackbar
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock

from api import img_url

Window.size=(360,640)
Builder.load_file('cards.kv')

class SwitchCommandeBtn(MDCard):
    shop=StringProperty()
    restau=StringProperty()
    current=ObjectProperty()


    def switch(self,current,old,screen,direction):
        pointer=self.ids.switch_bar
        if self.current != current:
            if direction=="left":
                anima=Animation(x=0,duration=1.5,t="out_elastic")
            else:
                right=pointer.right
                anima = Animation(x=right, duration=1.5, t="out_elastic")
            anima.start(pointer)


            current.icon_color="#ffffff"
            current.text_color="#ffffff"

            old.icon_color = "#1E1E1E"
            old.text_color = "#1E1E1E"

class SeeMoreBtn(MDCard):
    body=StringProperty('3 établissement')
    screen=ObjectProperty()

class ShopNearCard(MDCard):
    data = DictProperty({})
    logo=StringProperty('img/Carrefour Logo.jpg')
    nom=StringProperty("Carrefour")
    heure=StringProperty("ouvre à 10:00")


    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        print("enterrrr")
    pass
class ShopRangCard(MDCard):
    logo = StringProperty('img/kmc.png')
    nom = StringProperty("KMC")
    rang= StringProperty("img/rang 1.png")
    quartier=StringProperty("logbessus")
    rate = StringProperty("4.8")

class FoodCard(MDCard):
    in_menu=BooleanProperty(False)
    data=DictProperty({"nom":"Ndolé royale",'image':"img/ndolé.jpg","restaurant":"FPKA Foods","quartier":"logbessus","prix":"3500"})
    image=StringProperty(img_url)
class FoodDetail(MDBottomSheet):
    data = DictProperty(
        {"nom": "Ndolé royale", 'image': "img/ndolé.jpg", "restaurant": "FPKA Foods", "quartier": "logbessus",
         "prix": 3500})
    image = StringProperty(img_url)
    quantity = 1
    montant = 0

    def add_quantity(self):
        self.quantity += 1
        self.montant = self.quantity * self.data["prix"]
        print(self.montant)

    def reduice_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.montant = self.quantity * self.data["prix"]
        else:
            self.montant = self.data["prix"]
class ProductCard(MDCard):
    data=DictProperty({"nom":"Bouteille d’eau mineral 1L",'image':"img/ndolé.jpg","boutique":"Carrefour market","quartier":"bonamoussadi","prix":"500 fcfa"})
class BasketTitleCard(MDCard):
    restau=StringProperty()
    livraison=NumericProperty()
class BasketCard(MDCard):
    data=DictProperty({"nom":"Bouteille d’eau mineral 1L",'image':"img/ndolé.jpg","prix":500})
    quantity=1
    montant=0

    def add_quantity(self):
        self.quantity+=1
        self.montant =self.quantity * self.data["prix"]
        print(self.montant)
    def reduice_quantity(self):
        if self.quantity>1:
            self.quantity-=1
            self.montant =self.quantity * self.data["prix"]
        else:
            self.montant = self.data["prix"]

class RestauListItem(MDCard):
    data=DictProperty()
    livraison=StringProperty("1600")

kv="""
MDScreen:
    BoxLayout:
        orientation:"vertical"

        MDBoxLayout:
            id: box
            adaptive_height:True
            spacing:30
            padding:10
            pos_hint: {"center_x": .5, "center_y": .5}
            valign:"top"
            MDIconButton:
                icon: "account"
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": .5}
                theme_icon_color: "Custom"
                icon_color:"black"
                on_release: bottom_sheet.open()
    FoodDetail:
        id: bottom_sheet

"""

'''class App(MDApp):
    COLORS={
        "primary":"#A90404",
        "bg": "#ffffff",
        "light": "#D9D9D9",
        "normal": "#707070",
        "dark": "#1E1E1E",
    }
    def build(self):
        self.theme_cls.material_style = "M3"
        return Builder.load_string(kv)

App().run()'''