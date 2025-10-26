import datetime
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.metrics import dp
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

from api import userapi
from cards import ShopNearCard, FoodCard, ProductCard, RestauListItem,BasketTitleCard,BasketCard
from tools import LoadPage, NoWifi,LimitedScrollView,LimitedRV

Window.size=(360,640)
Builder.load_file('command.kv')



class MainCommand(MDScreen):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.get_commande()

    def get_commande(self):
        restaus=userapi.data.command["data"]
        restaus={"KMC_logbessus":{"livraison":14000,"command":[0,1,2,3]},"Carefour_logbessus":{"livraison":14000,"command":[0,1]}}
        print(self.ids)
        rv=self.ids["rv_commande"]
        rv.data=[]
        for restau in restaus.keys():
            rv.data.append(
                {
                    "viewclass":"BasketTitleCard",
                    "restau":restau,
                    "livraison":restaus[restau]["livraison"]
                }
            )
            for i in restaus[restau]["command"]:
                rv.data.append(
                    {
                        "viewclass": "BasketCard",

                    }
                )
    pass

"""
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
        self.screen=MainCommand()
    def build(self):
        return self.screen

asyncio.run(App().async_run(async_lib='asyncio'))"""