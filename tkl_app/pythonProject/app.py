
import asyncio
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager

from api import userapi
from authentification import AuthentificationPage
from acceuil import Home,SearchPage
from cards import FoodDetail
from command import MainCommand
from profile import MainProfil, EditProfil, HistoryProfil
from restaurant import RestaurantPage


Window.size=(360,640)
Builder.load_file('app.kv')


class HomeBottomNav(MDScreen):

    def deselect_all(self,btn,screen):
        childs=self.ids.box.children
        for child in childs:
            print(1)
            child.md_bg_color= "#D9D9D9"
            child.theme_icon_color= "Custom"
            child.icon_color= "#707070"
        btn.md_bg_color = "#A90404"
        btn.theme_icon_color = "Custom"
        btn.icon_color = "#ffffff"
        self.ids.sm.current=screen

    pass

class Splash(MDScreen):
    pass


class MainApp(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = MDScreenManager()
        self.screen_manager.add_widget(Splash(name="splash"))
        self.start()

    def login(self):
        self.screen_manager.add_widget(AuthentificationPage(name="authentification"))

    def useful_page(self):
        self.screen_manager.add_widget(HomeBottomNav(name="main"))

        self.screen_manager.add_widget(EditProfil(name="edit-profil"))
        self.screen_manager.add_widget(HistoryProfil(name="history-profil"))

        self.screen_manager.add_widget(RestaurantPage(name="restaurant"))
        self.screen_manager.current="splash"
        self.add_widget(self.screen_manager)
        self.bottom_sheet=FoodDetail()
        self.add_widget(self.bottom_sheet)

    def start(self):
        if userapi.me["connected"]:
            self.screen_manager.current="authentification"
        else:
            self.screen_manager.current = "main"

    def open_sheet(self,data):
        self.bottom_sheet.data=data
        self.bottom_sheet.open()

    def set_principal_screen(self,nom):
        main=self.screen_manager.get_screen("main")
        main.ids.sm.current=nom
        self.screen_manager.current = "main"

    def get_current(self):
        if self.screen_manager.current == "main":
            main = self.screen_manager.get_screen("main")
            return "main_"+main.ids.sm.current
        else:
            return self.screen_manager.current

    def go_to(self,nom):
        print("main_" in nom)
        if "main_" in nom:
            screen=nom.split("_")[1]
            self.set_principal_screen(screen)
        else:
            self.screen_manager.current =nom





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
        self.screen=MainApp()
    def build(self):
        return self.screen

asyncio.run(App().async_run(async_lib='asyncio'))
