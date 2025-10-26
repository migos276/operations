from kivy.animation import Animation
from kivy.properties import ObjectProperty, StringProperty, DictProperty, NumericProperty, BooleanProperty
from kivymd.app import MDApp
import asyncio
import os
import httpx
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard, MDCardSwipe
from kivymd.uix.label import MDLabel
from kivymd.uix.list import ThreeLineIconListItem, ThreeLineListItem
from kivymd.uix.snackbar import MDSnackbar
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock

from api import entreprise_api, restaurant_api

"""
from api import base_dir, delete_menu_plat"""

Window.size = (360, 640)
card_kv=os.path.join(entreprise_api.base_dir,"entreprise/cards.kv")
Builder.load_file(card_kv)


class ActiveCommandCard(MDCard):
    data=DictProperty({"id":10,"client":{"username":"Kieran"},"position":{"lieu":"logbessus"},"status":"préparation"})
    manager=ObjectProperty()
    pass
class CommandAskCard(MDCard):
    data=DictProperty({"id":10,"client":{"username":"Kieran"},"position":{"lieu":"logbessus"},"status":"préparation"})
    manager=ObjectProperty()
    pass


class MenuPlatCard(MDCard):
    data = DictProperty(
        {"image": "img/ndolé.jpg", "description":"un plat de Ndolé + 2 baton ", "prix": 3500, "nom": "ndolé royale"})
    manager = ObjectProperty()
    nom=StringProperty()
    image=""
    pass
class CurrentMenuPlatCard(MDCard):
    data = DictProperty(
        {"image": "img/ndolé.jpg", "description":"un plat de Ndolé + 2 baton ", "prix": 3500, "nom": "ndolé royale","rate":5},)
    manager = ObjectProperty()
    pass
class PlatCard(MDCard):
    selected = BooleanProperty(False)
    data = DictProperty()
    screen = ObjectProperty()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        print("card",self.data)
        self._long_press_event = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not self.screen.select:
                print("enter")
                self._long_press_event = Clock.schedule_once(self.long_press_action, 1)
                self.select_me()
                return True
            else:
                self.select_me()
        return super().on_touch_down(touch)

    def select_me(self):
        app = MDApp.get_running_app()
        if not self.screen.select:
            self.selected =False
        else:
            self.selected = not self.selected
            if self.selected:
                self.screen.select_item.append(self.index)
            else:
                self.screen.select_item.pop(self.index)
        self.md_bg_color = (169 / 255, 4 / 255, 4 / 255, .5) if self.selected else app.COLORS["light"]

    def on_touch_up(self, touch):
        # Si l'utilisateur lève le doigt avant 60s, annuler le long press
        print("stop")
        if self._long_press_event :
            if not self.screen.select:
                self._long_press_event.cancel()
                self._long_press_event = None

        return super().on_touch_up(touch)

    def long_press_action(self, dt):
        self.screen.select_mode()
        self._long_press_event = None
class MenuPlatSwipeToDeleteItem(MDCardSwipe):
    is_open=False
    data = DictProperty(
        {"image": "img/ndolé.jpg", "description": "un plat de Ndolé + 2 baton ", "prix": 3500, "nom": "ndolé royale"})
    manager = ObjectProperty()
    rv= ObjectProperty()
    nom = StringProperty()
    image = StringProperty("img/ndolé.jpg")
    index=NumericProperty()


    def open_me(self):
        if self.is_open:
            anim = Animation(open_progress=1, duration=0.25)
            anim.start(self)
            self.is_open = False
        else:
            # Sinon → l’ouvrir
            anim = Animation(open_progress=0.7, duration=0.25)
            anim.start(self)
            self.is_open = True
        return True
    def delete(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.delete_item()))

    async def delete_item(self):

        try:
            print(self.rv)
            response= await restaurant_api.delete_menu_plat(int(self.data["id"]))
            del self.rv.data[self.index]
            print("refresh 🤩🤗")

        except Exception as e:
            print("erreur",e)

class LivreurCard(MDCard):
    data=DictProperty({})

class HoraireCard(ThreeLineListItem):
    pass



kv = """
MDScreen:
    MDBoxLayout:
        orientation:"vertical"
        spacing:5
        HoraireCard:
        HoraireCard:


"""
"""
class App(MDApp):
    COLORS = {
        "primary": "#A90404",
        "bg": "#ffffff",
        "light": "#D9D9D9",
        "normal": "#707070",
        "dark": "#1E1E1E",
    }

    def build(self):
        self.theme_cls.material_style = "M3"
        return Builder.load_string(kv)


App().run()"""