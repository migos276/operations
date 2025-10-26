from fontTools.merge.util import first
from kivy.animation import Animation
from kivy.metrics import dp

from kivy.properties import ObjectProperty, NumericProperty, DictProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
import asyncio
import httpx
from kivymd.uix.filemanager import MDFileManager
import os

from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.textfield import MDTextField
from matplotlib.widgets import Button

from api import restaurant_api
from entreprise.cards import MenuPlatSwipeToDeleteItem,PlatCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineRightIconListItem, MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.snackbar import MDSnackbar
from kivy.core.window import Window
from kivy.metrics import sp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton,MDFlatButton
from kivy.clock import Clock

from tools import LoadPage

Builder.load_file("entreprise/restaurant/profile.kv")

btn_kv = """
MDRectangleFlatButton:
    text:"Créer"
    font_style:"Button"
    pos_hint:{"center_x":0.5,"center_y":.5}
    md_bg_color:"#A90404"
    line_color:(0,0,0,0)
    text_color:"#ffffff"
"""
topbar_kv = '''
MDBoxLayout:
    adaptive_height:True


'''
return_btn_kv = '''
MDIconButton:
    icon:"arrow-left"
    md_bg_color:app.COLORS["light"]
    theme_icon_color:"Custom"
    icon_color:app.COLORS["normal"]
    on_press:
        self.screen.go_back()
'''

add_btn_kv = '''
MDIconButton:
    icon:"plus"
    md_bg_color:app.COLORS["primary"]
    theme_icon_color:"Custom"
    icon_color:app.COLORS["bg"]
    pos_hint:{"right":.9,"y":.05}
    on_press:
        self.screen.add_plat()


'''

delete_btn_kv = '''
MDIconButton:
    icon:"trash-can"
    md_bg_color:0,0,0,0
    theme_icon_color:"Custom"
    icon_color:app.COLORS["normal"]
    on_press:
        self.screen.clear_menu()

'''

select_bar_kv = '''
MDBoxLayout:
    id:box
    adaptive_height:True
    pos_hint:{"right":1, "center_y": .5}
    padding:10
    spacing:15
    
    size_hint_x:.5
    md_bg_color:app.COLORS["light"]
    
    MDIconButton:
        icon:"close"
        md_bg_color:0,0,0,0
        theme_icon_color:"Custom"
        ripple_behavior: False
        icon_color:app.COLORS["normal"]
        on_press:root.screen.normal_mode()
        
    Widget:
    

    MDIconButton:
        icon:"trash-can"
        ripple_behavior: False
        md_bg_color:0,0,0,0
        theme_icon_color:"Custom"
        icon_color:app.COLORS["normal"]
        on_press:root.screen.delete_select_plat()
            
'''



search_kv = '''
MDCard:
    size_hint_x:.8
    pos_hint:{"center_x":0.5,"center_y":.5}
    radius:[35]
    height:"50dp"
    md_bg_color:app.COLORS["light"]
    elevation:0

    TextInput:
        id:search_bar
        hint_text:"rechercher un plat"
        icon_left:"magnify"
        size_hint_x:.8
        background_normal:""
        pos_hint:{"center_x":0.5,"center_y":.5}
        valign:"center"
        padding_y:(17,17)
        padding_x:10
        background_color:0,0,0,0 
        multiline:False
        on_text: 
            self.screen.search(self.text)
'''



class AllPlatPage(MDScreen):
    data=DictProperty({'plats': []})
    select=BooleanProperty(False)
    select_item=ListProperty([])
    items = ListProperty([])

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.first=True
        self.mainFloat = FloatLayout()
        self.box=MDBoxLayout(orientation="vertical",pos_hint={"center_x":0.5,"top":1})
        return_btn=Builder.load_string(return_btn_kv)
        return_btn.screen=self
        self.bar=MDFloatLayout(adaptive_size=True,size_hint_x=2,pos_hint={"x":0,"top":1})
        self.title=MDLabel(text="Tous les Plats",font_size=sp(16),bold=True,adaptive_height=True,halign="center",pos_hint={"center_x":0.5,"center_y":.5})
        self.topbar=MDBoxLayout(adaptive_height=True,pos_hint={"x":0,"center_y":.5},padding=10, size_hint_x=.5)
        self.topbar.add_widget(return_btn)
        self.topbar.add_widget(self.title)

        self.bar.add_widget(self.topbar)
        self.selectbar = Builder.load_string(select_bar_kv)
        self.selectbar.screen=self
        self.bar.add_widget(self.selectbar)
        self.box.add_widget(self.bar)

        self.recycleView = RvPlatCard()
        self.box.add_widget(self.recycleView)
        self.mainFloat.add_widget(self.box)
        add_btn = Builder.load_string(add_btn_kv)
        add_btn.screen = self
        self.mainFloat.add_widget(add_btn)
        self.add_widget(self.mainFloat)
        self.on_start()

    def delete_select_plat(self):
        for index in self.select_item:
            del self.recycleView.data[index]

    def select_mode(self):
        self.select=True
        value=self.bar.width/2
        anim=Animation(right=value,duration=1,t="in_out_cubic")
        anim.start(self.bar)

    def normal_mode(self):
        self.select = False
        anim=Animation(x=0,duration=1,t="in_out_cubic")
        anim.start(self.bar)

    def on_start(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.start()))
    def set_list_plat(self,data):
        print("data:",data)
        def add_icon_item(i,j):
            print("plats")
            print(i)
            self.recycleView.data.append(
                {
                    "viewclass": "PlatCard",
                    "data" : i,
                    "index":j,
                    "screen":self,

                }
            )

        self.recycleView.data=[]

        for i,plat in enumerate(data):
            print("plat",i,': ',plat)
            add_icon_item(plat,i)

    async def start(self):
        load = LoadPage()
        self.add_widget(load)
        data= await restaurant_api.get_all_plat()
        self.set_list_plat(data)
        self.remove_widget(load)

class RvPlatCard(MDRecycleView):
    col_number=NumericProperty(int((Window.width-10)/110))
    def __init__(self,**kwargs):
        super(RvPlatCard, self).__init__(**kwargs)
        self.data=[]
        print(Window.width)
        print(self.col_number)
    pass


class AddGlobalePlatPage(MDScreen):

    def add_plat(self,plat_id,nom,image,prix,description):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.add_plat_asynch(nom,image)))

    async def add_plat_asynch(self ,nom,image):
        await restaurant_api.create_plat(image,nom)


    def go_back(self):
        next = self.manager.get_screen("all-plat")
        next.set_list_livreur()
        self.manager.current = "all-plat"

    pass


class App(MDApp):
    COLORS = {
        "primary": "#A90404",
        "bg": "#ffffff",
        "light": "#D9D9D9",
        "normal": "#707070",
        "dark": "#1E1E1E",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Red"
        self.screen = AllPlatPage()
        self.saver = ObjectProperty()
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path, ext=['.jpg','.jpeg','.png']
        )
    def build(self):
        Window.size = (360, 640)
        print(Window.width)
        return self.screen

    def print_size(self, dt):
        print("Width:", Window.width, "Height:", Window.height)

    def file_manager_open(self,saver):
        self.file_manager.show(os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True
        self.saver=saver
    def change(self,widget):
        widget.text="TYYU"
    def exit_manager(self, *args):

        self.manager_open = False
        self.file_manager.close()
    def select_path(self, path: str):

        self.exit_manager()
        self.saver.source=path
        return True

asyncio.run(App().async_run(async_lib='asyncio'))