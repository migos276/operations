
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import asyncio
from kivy.clock import Clock
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.snackbar import MDSnackbar
from cards import SwitchCommandeBtn
from api import userapi
from tools import LoadPage, NoWifi

Window.size=(360,640)
Builder.load_file('profile.kv')

class Profil(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        screen_manager = ScreenManager()
        screen_manager.add_widget(MainProfil(name="main-profil"))
        screen_manager.add_widget(EditProfil(name="edit-profil"))
        screen_manager.add_widget(HistoryProfil(name="history-profil"))
        screen_manager.current="main-profil"
        print(screen_manager)
        self.add_widget(screen_manager)

class MainProfil(MDScreen):
    nom = StringProperty(userapi.me["username"].lower())
    om = StringProperty(userapi.data.paid["om"])
    momo = StringProperty(userapi.data.paid["momo"])
    pass
class EditProfil(MDScreen):
    print(userapi.my_info)
    nom = StringProperty(userapi.my_info["username"].lower())
    numero=StringProperty(str(userapi.my_info["tel"]))
    om=StringProperty(userapi.data.paid["om"])
    momo = StringProperty(userapi.data.paid["momo"])

    def go_back(self):
        self.manager.current="main-profil"

    def update(self,nom,tel,om,momo):
        if nom and tel:
            data={}
            if nom != self.nom:
                data["username"]=nom
            if tel != self.numero:
                data["tel"]=tel
            if data:
                Clock.schedule_once(lambda dt: asyncio.create_task(userapi.update_my_info(data)))
        else:
            MDSnackbar(
                MDLabel(
                    text="les champs nom d'utilisateur et un numéro à contacter sont obligatoire veuillez leurs remplir "
                )
            ).open()
        if not om:
            om="aucun"
        if not momo:
            momo="aucun"
        userapi.data.update_paid(om=om,momo=momo)
        print("good")

class HistoryProfil(MDScreen):
    pass




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
        self.screen=Profil()
    def build(self):
        return self.screen

asyncio.run(App().async_run(async_lib='asyncio'))'''