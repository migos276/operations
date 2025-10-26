from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.uix.image import Image
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

from api import userapi

Window.size=(412/1.5,917/1.5)
Builder.load_file('authentification.kv')

class AuthentificationPage(MDScreen):
    pass

class FirstTime(MDScreen):
    manager = ObjectProperty()
    pass

class Inscription(MDScreen):
    manager = ObjectProperty()
    def sign_in(self,nom,tel,email,password,confirm):
        if nom.error and tel.error and email.error and password.error and confirm.error:
            if nom.text and tel.text and email.text and password.text and confirm.text:
                if len(password)>=8:
                    if password == confirm:
                        data={"username":nom.text,"tel":int(tel.text),"email":email.text,"password":password.text}
                        Clock.schedule_once(lambda dt: asyncio.create_task(self.sign_in_data(data)))
                    else:
                        confirm.error=True

                else:
                    password.error=True
        else:
            MDSnackbar(
                MDLabel(
                    text="remplir correctement toutes les informations")
            ).open()
    async def sign_in_data(self, data):
        try:
            message = await userapi.sign_client(data=data)
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

    pass
    pass

class Connexion(MDScreen):
    manager = ObjectProperty()
    def login(self, email, password):
        if not (email.error or password.error) and email.text and password.text:
            Clock.schedule_once(lambda dt: asyncio.create_task(self.login_data(email.text, password.text)))

    async def login_data(self, email, password):
        try:
            message=await userapi.login_client(email=email,password=password)
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

    pass
'''
class App(MDApp):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Red"
        self.screen=AuthentificationPage()
    def build(self):
        return self.screen


asyncio.run(App().async_run(async_lib='asyncio'))'''