from kivy.properties import ObjectProperty
from kivymd.app import MDApp
import asyncio
import httpx
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton,MDFlatButton
from kivy.clock import Clock

from api import login_restaurant, login_livreur

Window.size=(360,640)
Builder.load_file('entreprise/restaurant/home.kv')

class AuthentificationPage(MDScreen):
    pass


class App(MDApp):
    COLORS = {
        "primary": "#A90404",
        "bg": "#fffff",
        "light": "#D9D9D9",
        "normal": "#707070",
        "dark": "#1E1E1E",
    }
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Red"
        self.screen=AuthentificationPage()
    def build(self):
        return self.screen


asyncio.run(App().async_run(async_lib='asyncio'))