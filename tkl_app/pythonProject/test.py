# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# Assure-toi d'avoir installé MapView (kivy_garden.mapview)
# Exemple d'import : pip install kivy-garden.mapview
from kivy_garden.mapview import MapView, MapMarker

class MapScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # Coordonnées Bonamoussadi (approx.)
        lat = 4.08919
        lon = 9.74278

        # Création de la MapView
        self.mapview = MapView(zoom=16, lat=lat, lon=lon)
        self.add_widget(self.mapview)

        # Ajout d'un marqueur (après que la map ait chargé)
        Clock.schedule_once(lambda dt: self.add_marker(lat, lon), 0.5)

    def add_marker(self, lat, lon):
        marker = MapMarker(lat=lat, lon=lon, source="")  # source vide => icône par défaut
        # tu peux mettre "marker.source='path/to/icon.png'" pour une icône perso
        self.mapview.add_marker(marker)
        # centre la carte précisément sur le marqueur
        self.mapview.center_on(lat, lon)

class BonamoussadiApp(App):
    def build(self):
        return MapScreen()

if __name__ == "__main__":
    BonamoussadiApp().run()
