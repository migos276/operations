from datetime import datetime,time

from fontTools.merge.util import first
from kivy.animation import Animation
from kivy.metrics import dp

from kivy.properties import ObjectProperty, NumericProperty, DictProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import CardTransition, WipeTransition
from kivymd.app import MDApp
import asyncio
import httpx
from kivymd.uix.filemanager import MDFileManager
import os

from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.textfield import MDTextField

from api import restaurant_api, entreprise_api, dailystat
from entreprise.cards import MenuPlatSwipeToDeleteItem,PlatCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineRightIconListItem, MDList, OneLineListItem, ThreeLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.snackbar import MDSnackbar
from kivy.core.window import Window
from kivy.metrics import sp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton,MDFlatButton
from kivy.clock import Clock

"""from api import my_restaurant, add_menu_hebdo, add_exist_plat_to_menu, add_new_plat_to_menu, search_plat, get_menu_plat, \
    clear_menu, get_my_restaurant_info"""
from tools import LoadPage, NoWifi

Window.size=(360,640)
Builder.load_file('profile.kv')
btn_kv="""
MDRectangleFlatButton:
    text:"Créer"
    font_style:"Button"
    pos_hint:{"center_x":0.5,"center_y":.5}
    md_bg_color:"#A90404"
    line_color:(0,0,0,0)
    text_color:"#ffffff"
"""
topbar_kv='''
MDBoxLayout:
    adaptive_height:True
    
    
'''
return_btn_kv='''
MDIconButton:
    icon:"arrow-left"
    md_bg_color:app.COLORS["light"]
    theme_icon_color:"Custom"
    icon_color:app.COLORS["normal"]
    on_press:
        self.screen.go_back()
'''

add_btn_kv='''
MDIconButton:
    icon:"plus"
    md_bg_color:app.COLORS["primary"]
    theme_icon_color:"Custom"
    icon_color:app.COLORS["bg"]
    pos_hint:{"right":.9,"y":.05}
    on_press:
        self.screen.add_plat()

    
'''

edit_btn_kv = '''
MDIconButton:
    icon:"pencil"
    md_bg_color:0,0,0,0
    theme_icon_color:"Custom"
    icon_color:app.COLORS["normal"]
    on_press:
        self.screen.edit()


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

search_kv='''
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

select_bar_kv = '''
MDBoxLayout:
    id:box
    opacity:0
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

class Profile(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        screen_manager=MDScreenManager()
        menu_hebdo = MenuHebdoPage(name="menu-hebdo")
        # on peut passer le manager explicitement
        menu_hebdo.manager_ref = screen_manager
        screen_manager.add_widget(MainProfile(name="main"))
        screen_manager.add_widget(menu_hebdo)
        screen_manager.add_widget(DayPage(name="menu"))
        screen_manager.add_widget(AddPlatPage(name="ajouter-plat"))
        screen_manager.add_widget(SearchPlatPage(name="selectionner-plat"))
        screen_manager.add_widget(StaticMenuPage(name="menu-static"))
        screen_manager.add_widget(AddStaticPlatPage(name="ajouter-plat-static"))
        screen_manager.add_widget(AllPlatPage(name="global-plat"))
        screen_manager.add_widget(AddGlobalePlatPage(name="ajouter-plat-global"))
        screen_manager.add_widget(LivreurPage(name="livreur"))
        screen_manager.add_widget(AddLivreurPage(name="ajouter-livreur"))
        screen_manager.add_widget(HorairePage(name="horaire"))
        screen_manager.add_widget(EditHorairePage(name="edit-horaire"))
        screen_manager.current="main"
        screen_manager.transition= WipeTransition(duration=0.5)
        self.add_widget(screen_manager)

    pass


class MainProfile(MDScreen):
    total_vente=NumericProperty(0)
    total_montant = NumericProperty(0)
    rate= NumericProperty(0)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.total_montant=dailystat.data["montant_gagne"]
        self.total_vente=dailystat.data["plats_vendus"]
        self.rate=restaurant_api.my_restaurant['rate']
    pass

#----------------------------------Menu Hebdomadaire----------------------------------->

class DayCard(TwoLineRightIconListItem):
    day=StringProperty()
    manager=ObjectProperty()
    data=DictProperty()

    def go_to_day_page(self):
        next_screen = self.manager.get_screen("menu")
        next_screen.data = self.data["menu"]
        next_screen.jour = self.day
        self.manager.current = "menu"
class MenuHebdoPage(MDScreen):

    jours={"lundi":{},"mardi":{},"mercredi":{},"jeudi":{},"vendredi":{},"samedi":{},"dimanche":{}}
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.box=MDBoxLayout(orientation="vertical",pos_hint={"center_x":0.5,"top":1})
        return_btn=Builder.load_string(return_btn_kv)
        return_btn.screen=self
        title=MDLabel(text="Menu Hebdomadaire",font_size=sp(16),bold=True,adaptive_height=True,halign="center",pos_hint={"center_x":0.5,"center_y":.5})
        self.topbar=MDBoxLayout(adaptive_height=True,pos_hint={"center_x":0.5,"center_y":.5},padding=10)
        self.topbar.add_widget(return_btn)
        self.topbar.add_widget(title)
        self.scrollview=MDScrollView()
        self.list=MDList()


    def on_enter(self, *args):
        self.on_start()

    def on_start(self):
        self.clear_widgets()
        if restaurant_api.my_restaurant and restaurant_api.my_restaurant["menu_hebdo"]!=None:
            print("restauuuuuuu ",restaurant_api.my_restaurant)
            self.get_day()
        else:
            self.first_time()

    def get_day(self):
        load = LoadPage()
        self.add_widget(load)
        self.box.clear_widgets()
        self.box.add_widget(self.topbar)
        self.scrollview.clear_widgets()
        self.list.clear_widgets()
        menus=restaurant_api.my_restaurant["menu_hebdo"]["menus"]
        for menu in menus:
            j=menu["jour"]
            self.jours[j]["menu"]=menu
        for heure in restaurant_api.my_restaurant["horaire"]["horaires"]:
            j = heure["jour"]
            self.jours[j]["heure"] = heure
        print(self.jours)
        self.list.clear_widgets()
        for jour in self.jours.keys():
            print(self.manager)
            element=DayCard(day=jour,data=self.jours[jour],manager=self.manager)
            self.list.add_widget(element)
        self.box.adaptive_height = False
        self.scrollview.add_widget(self.list)
        self.box.add_widget(self.scrollview)
        self.add_widget(self.box)
        self.remove_widget(load)

    def create_menu_hebdo(self,instance):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.create_menu_hebdo_ascyn()))

    async def create_menu_hebdo_ascyn(self):
        load=LoadPage()
        self.add_widget(load)
        await restaurant_api.add_menu_hebdo()
        self.on_start()

    def first_time(self):
        self.box.clear_widgets()
        self.box.add_widget(self.topbar)
        bouton=Builder.load_string(btn_kv)
        bouton.bind(on_press=self.create_menu_hebdo)
        self.box.adaptive_height=True
        self.add_widget(self.box)
        self.add_widget(bouton)
    def go_back(self):
        self.manager.current = "main"

class RvCard(MDRecycleView):
    def __init__(self,**kwargs):
        super(RvCard, self).__init__(**kwargs)
        self.data=[]
    pass

class DayPage(MDScreen):
    data=DictProperty({'plats': []})
    jour=StringProperty()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.first=True
        mainFloat = FloatLayout()
        self.box=MDBoxLayout(orientation="vertical",pos_hint={"center_x":0.5,"top":1})
        return_btn=Builder.load_string(return_btn_kv)
        return_btn.screen=self
        clear_btn= Builder.load_string(delete_btn_kv)
        clear_btn.screen=self
        self.title=MDLabel(text="",font_size=sp(16),bold=True,adaptive_height=True,halign="center",pos_hint={"center_x":0.5,"center_y":.5})
        topbar=MDBoxLayout(adaptive_height=True,pos_hint={"center_x":0.5,"center_y":.5},padding=10)
        topbar.add_widget(return_btn)
        topbar.add_widget(self.title)
        topbar.add_widget(clear_btn)
        self.box.add_widget(topbar)
        self.recycleView = RvCard()
        self.box.add_widget(self.recycleView)
        mainFloat.add_widget(self.box)
        add_btn = Builder.load_string(add_btn_kv)
        add_btn.screen=self
        mainFloat.add_widget(add_btn)
        self.add_widget(mainFloat)

    def on_enter(self, *args):
        self.title.text=self.jour.capitalize()
        if self.first:
            print("first")
            self.set_list_plat()
            Clock.schedule_once(lambda dt: self.recycleView.refresh_from_data(), 0.1)
            self.first=False
        else:
            self.recycleView.refresh_from_data()


    def set_list_plat(self):

        def add_icon_item(i,j):
            print("plats")
            print(i)
            self.recycleView.data.append(
                {
                    "viewclass": "MenuPlatSwipeToDeleteItem",
                    "data" : i,
                    "nom":i["plat"]["plat"]["nom"].capitalize(),
                    "image":i["plat"]["image"],
                    "rv":self.recycleView,
                    "index":j
                }
            )

        self.recycleView.data.clear()
        for i,plat in enumerate(self.data["plats"]):
            add_icon_item(plat,i)


    def go_back(self):
        self.manager.current="menu-hebdo"
    def add_plat(self):
        next = self.manager.get_screen("ajouter-plat")
        next.data = self.data
        next.menu=self.data["id"]
        self.manager.current = "ajouter-plat"

    def clear_menu(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.clear_item()))

    async def clear_item(self):

        try:
            await restaurant_api.clear_menu(self.data["id"])
            self.recycleView.data.clear()
            self.recycleView.refresh_from_data()

        except Exception as e:
            print("erreur", e)

class AddPlatPage(MDScreen):
    data=DictProperty()
    check="select"
    menu=NumericProperty(1)
    def get_check(self,instance, value, topping):
        if value:
            self.check=topping
            print("check: ",self.check)

    def add_plat(self,plat_id,nom,image,prix,description):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.add_plat_asynch(plat_id,nom,image,prix,description)))

    async def add_plat_asynch(self,plat_id,nom,image,prix,description):
        if self.check=="select":
            await restaurant_api.add_exist_plat_to_menu(menu=self.menu,plat_id=plat_id,prix=prix,description=description)
        else :
            await restaurant_api.add_new_plat_to_menu(menu=self.menu,image=image,nom=nom,prix=prix,description=description)


    async def go_back_async(self):
        data=await restaurant_api.get_menu_plat(self.menu)
        print(data)
        next = self.manager.get_screen("menu")
        jour=data.pop("jour")
        next.data = data
        next.jour = jour
        self.manager.current = "menu"

    def go_back(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.go_back_async()))


    pass

class SearchItem(OneLineListItem):
    padding=0
    adaptive_height=True
    pass
class SearchPlatPage(MDScreen):
    saver=ObjectProperty()
    prev_name=StringProperty()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        mainFloat = FloatLayout()
        self.box=MDBoxLayout(orientation="vertical",pos_hint={"center_x":0.5,"top":1})
        return_btn=Builder.load_string(return_btn_kv)
        return_btn.screen=self
        search_card=Builder.load_string(search_kv)
        self.search_bar=search_card.ids["search_bar"]
        self.search_bar.screen=self
        topbar = MDBoxLayout(adaptive_height=True, pos_hint={"center_x": 0.5, "center_y": .5}, padding=dp(10),spacing=dp(10))
        topbar.add_widget(return_btn)
        topbar.add_widget(search_card)
        self.box.add_widget(topbar)
        self.recycleView = RvCard()
        self.box.add_widget(self.recycleView)
        self.add_widget(self.box)

    def on_enter(self, *args):
        self.start()

    def go_back(self):
        self.manager.current = self.prev_name

    def set_list_plats(self, plats=[]):
        """Builds a list of icons for the screen MDIcons."""
        print(plats)
        def add_item(plat):
            self.recycleView.data.append(
                {
                    "viewclass": "SearchItem",
                    "text": plat["plat"]["nom"].capitalize(),
                    "on_release": lambda dt=plat: self.select(text=dt["plat"]["nom"],id=str(dt["id"])),
                }
            )

        self.recycleView.data = []
        for plat in plats:
            add_item(plat)

    async def search_data(self, text=""):
        plats=await restaurant_api.search_plat(text)
        print("text= ",text,"... plats= ",plats)
        self.set_list_plats(plats=plats)
        await asyncio.sleep(1)


    def search(self,text):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.search_data(text=text)))


    def start(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.search_data()))

    def select(self,text,id):
        self.saver.text=text
        self.saver.value = id
        self.go_back()


#----------------------------------Menu Courant----------------------------------->

class StaticMenuPage(MDScreen):
    data=DictProperty({'plats': []})

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.first=True
        self.mainFloat = FloatLayout()
        self.box=MDBoxLayout(orientation="vertical",pos_hint={"center_x":0.5,"top":1})
        return_btn=Builder.load_string(return_btn_kv)
        return_btn.screen=self
        clear_btn= Builder.load_string(delete_btn_kv)
        clear_btn.screen=self
        self.title=MDLabel(text="Menu Constant",font_size=sp(16),bold=True,adaptive_height=True,halign="center",pos_hint={"center_x":0.5,"center_y":.5})
        self.topbar=MDBoxLayout(adaptive_height=True,pos_hint={"center_x":0.5,"center_y":.5},padding=10)
        self.topbar.add_widget(return_btn)
        self.topbar.add_widget(self.title)
        self.topbar.add_widget(clear_btn)

        self.recycleView = RvCard()
        self.on_start()

    def on_enter(self, *args):
        if restaurant_api.my_restaurant and restaurant_api.my_restaurant["menu_statique"] :
            if self.first:
                print("first")
                self.set_list_plat()
                Clock.schedule_once(lambda dt: self.recycleView.refresh_from_data(), 0.1)
                self.first = False
            else:
                self.recycleView.refresh_from_data()
    def on_start(self, *args):
        self.clear_widgets()
        if restaurant_api.my_restaurant and restaurant_api.my_restaurant["menu_statique"] :
            self.data=restaurant_api.my_restaurant["menu_statique"]
            print("data",self.data)
            self.already_have_a_menu()
            if self.first:
                print("first")
                self.set_list_plat()
                Clock.schedule_once(lambda dt: self.recycleView.refresh_from_data(), 0.1)
                self.first=False
            else:
                self.recycleView.refresh_from_data()

        else:
            self.first_time()


    def set_list_plat(self):

        def add_icon_item(i,j):
            print("plats")
            print(i)
            self.recycleView.data.append(
                {
                    "viewclass": "MenuPlatSwipeToDeleteItem",
                    "data" : i,
                    "nom":i["plat"]["plat"]["nom"].capitalize(),
                    "image":i["plat"]["image"],
                    "rv":self.recycleView,
                    "index":j
                }
            )

        self.recycleView.data.clear()
        self.data=restaurant_api.my_restaurant["menu_statique"]

        for i,plat in enumerate(self.data["plats"]):
            add_icon_item(plat,i)

    def first_time(self):
        self.box.clear_widgets()
        self.box.add_widget(self.topbar)
        bouton=Builder.load_string(btn_kv)
        bouton.bind(on_press=self.create_static_menu)
        self.box.adaptive_height=True
        self.add_widget(self.box)
        self.add_widget(bouton)

    def create_static_menu(self,instance):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.create_static_menu_ascyn()))

    async def create_static_menu_ascyn(self):
        load=LoadPage()
        self.add_widget(load)
        await restaurant_api.add_static_menu()
        self.on_start()

    def already_have_a_menu(self):
        self.box.clear_widgets()
        self.box.add_widget(self.topbar)
        self.box.add_widget(self.recycleView)
        self.mainFloat.add_widget(self.box)
        add_btn = Builder.load_string(add_btn_kv)
        add_btn.screen = self
        self.mainFloat.add_widget(add_btn)
        self.add_widget(self.mainFloat)


    def go_back(self):
        self.manager.current="main"
    def add_plat(self):
        next = self.manager.get_screen("ajouter-plat-static")
        next.data = self.data
        next.menu=self.data["id"]
        self.manager.current = "ajouter-plat-static"

    def clear_menu(self):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.clear_item()))

    async def clear_item(self):

        try:
            await restaurant_api.clear_static_menu(self.data["id"])
            self.recycleView.data.clear()
            self.recycleView.refresh_from_data()

        except Exception as e:
            print("erreur", e)


class AddStaticPlatPage(MDScreen):
    data=DictProperty()
    check="select"
    menu=NumericProperty(1)
    def get_check(self,instance, value, topping):
        if value:
            self.check=topping
            print("check: ",self.check)

    def add_plat(self,plat_id,nom,image,prix,description):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.add_plat_asynch(plat_id,nom,image,prix,description)))

    async def add_plat_asynch(self,plat_id,nom,image,prix,description):
        if self.check=="select":
            await restaurant_api.add_exist_static_plat_to_menu(menu=self.menu,plat_id=plat_id,prix=prix,description=description)
        else :
            await restaurant_api.add_new_static_plat_to_menu(menu=self.menu,image=image,nom=nom,prix=prix,description=description)



    def go_back(self):
        next = self.manager.get_screen("menu-static")
        next.set_list_livreur()
        self.manager.current = "menu-static"

    pass

#----------------------------------Tous les plats----------------------------------->
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


    def on_enter(self, *args):
        self.on_start()
    def delete_select_plat(self):
        for index in self.select_item:
            del self.recycleView.data[index]

    def select_mode(self):
        self.select=True
        value=self.bar.width/2
        anim=Animation(right=value,duration=1,t="in_out_cubic")
        anim2=Animation(opacity=1,duration=1,t="linear")
        anim2.start(self.selectbar)
        anim.start(self.bar)

    def normal_mode(self):
        self.select = False
        anim=Animation(x=0,duration=1,t="in_out_cubic")
        anim2 = Animation(opacity=0, duration=1, t="linear")
        anim2.start(self.selectbar)
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

    def go_back(self):
        self.manager.current = "main"

    def add_plat(self):
        self.manager.current = "ajouter-plat-global"

class RvPlatCard(MDRecycleView):
    col_number=NumericProperty(int((Window.width-10)/110))
    def __init__(self,**kwargs):
        super(RvPlatCard, self).__init__(**kwargs)
        self.data=[]
        print(Window.width)
        print(self.col_number)
    pass


class AddGlobalePlatPage(MDScreen):

    def add_plat(self,nom,image):
        Clock.schedule_once(lambda dt: asyncio.create_task(self.add_plat_asynch(nom,image)))

    async def add_plat_asynch(self ,nom,image):
        await restaurant_api.create_plat(image,nom)


    def go_back(self):
        self.manager.current = "global-plat"

    pass

#----------------------------------Livreurs----------------------------------->

class LivreurPage(MDScreen):
    data = ListProperty( [])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first = True
        self.mainFloat = FloatLayout()
        self.box = MDBoxLayout(orientation="vertical", pos_hint={"center_x": 0.5, "top": 1})
        return_btn = Builder.load_string(return_btn_kv)
        return_btn.screen = self

        self.title = MDLabel(text="Livreurs", font_size=sp(16), bold=True, adaptive_height=True, halign="center",
                             pos_hint={"center_x": 0.5, "center_y": .5})
        self.topbar = MDBoxLayout(adaptive_height=True, pos_hint={"center_x": 0.5, "center_y": .5}, padding=10)
        self.topbar.add_widget(return_btn)
        self.topbar.add_widget(self.title)
        self.box.add_widget(self.topbar)

        self.recycleView = RvCard()
        self.box.add_widget(self.recycleView)
        self.mainFloat.add_widget(self.box)
        add_btn = Builder.load_string(add_btn_kv)
        add_btn.screen = self
        self.mainFloat.add_widget(add_btn)
        self.add_widget(self.mainFloat)
        self.set_list_livreur()

    def on_enter(self, *args):

        self.set_list_livreur()

    def on_start(self, *args):
        self.clear_widgets()
        self.set_list_livreur()


    def set_list_livreur(self):

        def add_icon_item(i, j):
            print("livreurs")
            print(i)
            self.recycleView.data.append(
                {
                    "viewclass": "LivreurCard",
                    "data": i,
                    "rv": self.recycleView,
                    "index": j
                }
            )

        self.recycleView.data.clear()
        self.data = restaurant_api.my_restaurant["livreurs"]

        if self.data:
            for i in self.data:
                add_icon_item(self.data[i], i)
        else:
            self.recycleView.data.append(
                {
                    "viewclass": "MDLabel",
                    "text": "Aucun livreur",
                    "halign":"center",
                    "valign":"middle",
                    "color":"#707070"

                }
            )



    def go_back(self):
        self.manager.current = "main"

    def add_plat(self):
        self.manager.current = "ajouter-livreur"

class AddLivreurPage(MDScreen):
    qrcode=StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.qrcode=entreprise_api.generate_qrcode()




    def go_back(self):
        self.manager.current = "livreur"

    pass



#----------------------------------Horaires----------------------------------->

class HorairePage(MDScreen):

    jours={"lundi":{},"mardi":{},"mercredi":{},"jeudi":{},"vendredi":{},"samedi":{},"dimanche":{}}
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.box=MDBoxLayout(orientation="vertical",pos_hint={"center_x":0.5,"top":1})
        return_btn=Builder.load_string(return_btn_kv)
        return_btn.screen=self
        title=MDLabel(text="Menu Hebdomadaire",font_size=sp(16),bold=True,adaptive_height=True,halign="center",pos_hint={"center_x":0.5,"center_y":.5})
        edit_btn=Builder.load_string(edit_btn_kv)
        edit_btn.screen=self
        self.topbar=MDBoxLayout(adaptive_height=True,pos_hint={"center_x":0.5,"center_y":.5},padding=10)
        self.topbar.add_widget(return_btn)
        self.topbar.add_widget(title)
        self.topbar.add_widget(edit_btn)
        self.scrollview=MDScrollView()
        self.list=MDList()


    def on_enter(self, *args):
        self.clear_widgets()
        self.get_horaire()

    def get_horaire(self):
        load = LoadPage()
        self.add_widget(load)
        self.box.clear_widgets()
        self.box.add_widget(self.topbar)
        self.scrollview.clear_widgets()
        self.list.clear_widgets()
        horaires=restaurant_api.my_restaurant["horaire"]["horaires"]
        for horaire in horaires:
            j=horaire["jour"]
            self.jours[j]=horaire
        print(self.jours)
        self.list.clear_widgets()
        for jour in self.jours.keys():
            print(self.manager)
            element=ThreeLineListItem()
            element.text=jour
            element.secondary_text="ouverture: "+str(self.jours[jour]["ouverture"])
            element.tertiary_text="fermeture: "+str(self.jours[jour]["fermeture"])
            self.list.add_widget(element)
        self.box.adaptive_height = False
        self.scrollview.add_widget(self.list)
        self.box.add_widget(self.scrollview)
        self.add_widget(self.box)
        self.remove_widget(load)


    def go_back(self):
        self.manager.current = "main"

    def edit(self):
        self.manager.current = "edit-horaire"

class EditHorairePage(MDScreen):
    jours = {"lundi": {}, "mardi": {}, "mercredi": {}, "jeudi": {}, "vendredi": {}, "samedi": {}, "dimanche": {}}
    select_day=ListProperty([])
    saver=ObjectProperty()
    time_slect=StringProperty()
    select_time=BooleanProperty(False)

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.on_start()

    def on_enter(self, *args):
        self.on_start()

    def on_start(self):
        horaires = restaurant_api.my_restaurant["horaire"]["horaires"]
        print(horaires)
        for horaire in horaires:
            print(horaire)
            j = horaire["jour"]
            self.jours[j]=horaire["id"]
        print(self.jours)

    def update_horaire(self,ouverture,fermeture):
        if self.select_day:
            Clock.schedule_once(lambda dt: asyncio.create_task(self.update_horaire_async(ouverture,fermeture)))
        else:
            MDSnackbar(
                MDLabel(
                    text="choisir au moins un jour pour cette horaire"
                )
            ).open()

    async def update_horaire_async(self,ouverture,fermeture):
        data={"ouverture":ouverture,"fermeture":fermeture}
        for day in self.select_day:
            await restaurant_api.update_horaire(self.jours[day],data)
        ouverture=""
        fermeture=""


    def show_time_picker(self,saver):
        if not self.select_time:
            self.select_time=True
            time_dialog = MDTimePicker()
            self.saver=saver
            self.time_slect=time(0,0).strftime("%H:%M")
            time_dialog.bind(time=self.get_time)
            time_dialog.open()
            time_dialog.bind(on_dismiss=self.set_saver)

    def set_saver(self,instance):
        self.saver.text=self.time_slect
        self.saver=ObjectProperty()
        self.select_time = False
    def get_time(self, instance, time):
        self.time_slect=str(time)

        return time

    def get_select_day(self,select,value):
        if select:
            self.select_day.append(value)
        else:
            if value in self.select_day:
                self.select_day.remove(value)
        print(self.select_day)
    pass
    def go_back(self):
        self.manager.current = "horaire"


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
        self.screen = Profile()
        self.saver = ObjectProperty()
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path, ext=['.jpg','.jpeg','.png']
        )
    def build(self):
        return self.screen

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