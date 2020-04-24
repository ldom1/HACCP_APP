import json
import time

import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

from pyScripts.operations_etiquette import ManageEtiquetteScreen
from pyScripts.operations_friteuse import ManageFriteuseScreen
from pyScripts.operations_plan_nettoyage import ManagePlanNettoyageScreen
from pyScripts.operations_reception_produit import ManageReceptionProduitScreen
from pyScripts.operations_tracabilite import ManageTracabiliteScreen
from pyScripts.settings_categorie import ManageCategories
from pyScripts.settings_collaborateur import ManageCollaborateurs
from pyScripts.settings_element_refrigerant import ManageElementRefrigerant
from pyScripts.settings_etiquette import ManageEtiquette
from pyScripts.settings_fournisseur import ManageFournisseurs
from pyScripts.settings_friteuse import ManageFriteuse
from pyScripts.settings_lieu import ManageLieu
from pyScripts.settings_plan_nettoyage import ManagePlanNettoyage
from pyScripts.operations_temperature_frigidaire import ManageTemperatureFridgeScreen


class HomeScreen(Screen):
    pass


class TemperatureFrigoScreen(Screen):
    pass


class PlanNettoyageScreen(Screen):
    pass


class ReceptionProduitScreen(Screen):
    pass


class FriteuseScreen(Screen):
    pass


class EtiquetteScreen(Screen):
    pass


class TracabiliteScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class SettingsCollaborateursScreen(Screen):
    pass


class SettingsElementsRefrigerantsScreen(Screen):
    pass


class SettingsPlanNettoyageScreen(Screen):
    pass


class SettingsFournisseursScreen(Screen):
    pass


class SettingsFriteuseScreen(Screen):
    pass


class SettingsEtiquettesScreen(Screen):
    pass


class CameraScreen(Screen):

    def capture(self):
        app = App.get_running_app()

        camera = self.ids['camera']
        timestr = time.strftime("%H%M%S%d%m%Y")
        source = "img/img_etiquette_{}.png".format(timestr)
        print(self.ids['camera'].size)
        camera.export_to_png(filename=source, scale=self.ids['camera'].size)
        time.sleep(1)
        print("Captured")

        app.change_screen("operations_tracabilite_screen", direction="right")
        img_to_display = app.root.ids["operations_tracabilite_screen"].ids["img_tracabilite_to_display"]
        img_to_display.source = source


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(Button, Label):
    pass


class CameraClick(BoxLayout):
    pass


GUI = Builder.load_file("main.kv")


class MainApp(App):
    def build(self):
        return GUI

    def load_data(self):

        url_settings = "https://haccpapp-40c63.firebaseio.com/test_user/settings/.json"
        response = requests.get(url=url_settings)
        data_settings = json.loads(response.content.decode())
        return data_settings

    def on_start(self):
        data_settings = self.load_data()

        collaborateur = ManageCollaborateurs()
        collaborateur.load_operations(data=data_settings)
        collaborateur.load_settings(data=data_settings)

        element_refrigerant = ManageElementRefrigerant()
        element_refrigerant.load_operations(data=data_settings)
        element_refrigerant.load_settings(data=data_settings)

        lieu = ManageLieu()
        lieu.load_operations(data=data_settings)
        lieu.load_settings(data=data_settings)

        plan_nettoyage = ManagePlanNettoyage()
        plan_nettoyage.load_operations(data=data_settings)
        plan_nettoyage.load_settings(data=data_settings)

        fournisseur = ManageFournisseurs()
        fournisseur.load_operations(data=data_settings)
        fournisseur.load_settings(data=data_settings)

        start_time = time.time()
        categorie = ManageCategories()
        categorie.load_operations(data=data_settings)
        categorie.load_settings(data=data_settings)

        friteuse = ManageFriteuse()
        friteuse.load_operations(data=data_settings)
        friteuse.load_settings(data=data_settings)

        etiquette = ManageEtiquette()
        etiquette.load_operations(data=data_settings)
        etiquette.load_settings(data=data_settings)

    def change_screen(self, screen_name, direction):
        # Clean selected screen
        if screen_name == "operations_temperature_frigo_screen":
            ManageTemperatureFridgeScreen().clear_screen()
        elif screen_name == "operations_plan_nettoyage_screen":
            ManagePlanNettoyageScreen().clear_screen()
        elif screen_name == "operations_reception_produit_screen":
            ManageReceptionProduitScreen().clear_screen()
        elif screen_name == "operations_friteuse_screen":
            ManageFriteuseScreen().clear_screen()
        elif screen_name == "operations_etiquette_screen":
            ManageEtiquetteScreen().clear_screen()
        elif screen_name == "operations_etiquette_screen":
            ManageTracabiliteScreen().clear_screen()
        # Get the screen manager from kv file
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition.direction = direction
        screen_manager.current = screen_name  # change current to the screen name I pass


MainApp().run()
