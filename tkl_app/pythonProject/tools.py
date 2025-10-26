from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView


class LoadPage(FloatLayout):
    pass


class NoWifi(FloatLayout):
    fonction = StringProperty()
    screen=ObjectProperty()

    def destroy_widget(self):
        if self.parent:
            self.parent.remove_widget(self)
            self.screen.on_start()

    def fade_out(self):
        anim = Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=lambda *x: self.destroy_widget())
        anim.start(self)

    pass

class LimitedScrollView(MDScrollView):
    limit_scroll = BooleanProperty(True)

    def on_scroll_y(self, instance, value):
        if self.limit_scroll:
            # scroll_y varie de 0 (bas) à 1 (haut)
            if value < 0:
                self.scroll_y = 0
            elif value > 1:
                self.scroll_y = 1

    def on_scroll_x(self, instance, value):
        if self.limit_scroll:
            # scroll_y varie de 0 (bas) à 1 (haut)
            if value < 0:
                self.scroll_x= 0
            elif value > 1:
                self.scroll_x = 1


class LimitedRV(RecycleView):
    limit_scroll = BooleanProperty(True)

    def on_scroll_y(self, instance, value):
        if self.limit_scroll:
            # scroll_y va de 0 (bas) à 1 (haut)
            if value < 0:
                self.scroll_y = 0
            elif value > 1:
                self.scroll_y = 1



KV = '''
<LoadPage>
    FloatLayout:
        pos_hint: {"top":1, "center_x":.5}  
        background_normal:""
        background_color:"#000000"
        padding:5
        canvas.before:
            Color:
                rgba:app.theme_cls.bg_dark if app.theme_cls.theme_style=="Dark" else app.theme_cls.bg_light
            Rectangle:
                pos:self.pos
                size:self.size
        MDSpinner:
            size_hint: .2, .2
            pos_hint: {'center_x': .5, 'center_y': .5}
            palette:
                [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1], \
                [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1], \
                [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1], \
                [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],

            determinate: False
<NoWifi>: 
    pos_hint: {"top":1, "center_x":.5}  
    background_normal:""
    background_color:"#000000"
    padding:5
    canvas.before:
        Color:
            rgba:app.theme_cls.bg_dark if app.theme_cls.theme_style=="Dark" else app.theme_cls.bg_light
        Rectangle:
            pos:self.pos
            size:self.size
    Image:
        id:img
        padding:0
        md_bg_color:"#000000"
        source:"img/no_wifi.png"
        size_hint:(.5,.5)
        keep_ratio:True
        pos_hint: {"top":.9, "center_x":.5}
    MDBoxLayout:
        pos_hint: {"center_x":.5}
        y:img.y-(self.height/2)
        orientation:'vertical'
        adaptive_height:True
        padding:10
        spacing:10
        MDLabel:
            text:'Oups,un probléme est survenu'
            bold:True
            font_size:18
            adaptive_height:True
            halign:'center'
        MDLabel:
            text:'merci de faire une nouvelle tentative dans quelques secondes'
            font_size:14
            adaptive_height:True
            halign:'center'
        MDFlatButton:
            id:but
            text:'Réessayer'
            radius:[15]
            padding:15
            md_bg_color:app.COLORS["primary"]
            pos_hint:{"center_x":.5}
            on_press:root.fade_out()

'''

Builder.load_string(KV)
