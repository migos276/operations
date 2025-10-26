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

from api import entreprise_api

"""
from api import login_restaurant, login_livreur"""

Window.size=(360,640)
Builder.load_file('authentification.kv')

class AuthentificationPage(MDScreen):
    pass

class FirstTime(MDScreen):
    manager = ObjectProperty()
    pass

class ConnexionEntreprise(MDScreen):
    manager = ObjectProperty()
    def login(self, code):
        if not code.error and code.text:
            Clock.schedule_once(lambda dt: asyncio.create_task(self.login_data(code.text)))

    async def login_data(self,code):
        try:
            async with (httpx.AsyncClient() as client):
                message=await entreprise_api.login_restaurant(code)
                MDSnackbar(
                    MDLabel(
                        text=str(message)
                    )
                ).open()
        except Exception as e:
            print(e)
            MDSnackbar(
                MDLabel(
                    text=str(e)
                )
            ).open()

class ConnexionLivreur(MDScreen):
    manager = ObjectProperty()
    def login(self, email, password):
        if not (email.error or password.error) and email.text and password.text:
            Clock.schedule_once(lambda dt: asyncio.create_task(self.login_data(email.text, password.text)))

    async def login_data(self, email, password):
        try:
            async with (httpx.AsyncClient() as client):
                #message=await login_livreur(email=email,password=password)
                MDSnackbar(
                    MDLabel(
                        text=str("message")
                    )
                ).open()
        except Exception as e:
            print(e)
            MDSnackbar(
                MDLabel(
                    text=str(e)
                )
            ).open()

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