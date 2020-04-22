import json

import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image

from HaccpApp.haccpApp.src.pyScripts.operations_etiquette import ManageEtiquetteScreen
from HaccpApp.haccpApp.src.pyScripts.operations_friteuse import ManageFriteuseScreen
from HaccpApp.haccpApp.src.pyScripts.operations_plan_nettoyage import ManagePlanNettoyageScreen
from HaccpApp.haccpApp.src.pyScripts.operations_reception_produit import ManageReceptionProduitScreen
from HaccpApp.haccpApp.src.pyScripts.settings_categorie import ManageCategories
from HaccpApp.haccpApp.src.pyScripts.settings_collaborateur import ManageCollaborateurs
from HaccpApp.haccpApp.src.pyScripts.settings_element_refrigerant import ManageElementRefrigerant
from HaccpApp.haccpApp.src.pyScripts.settings_etiquette import ManageEtiquette
from HaccpApp.haccpApp.src.pyScripts.settings_fournisseur import ManageFournisseurs
from HaccpApp.haccpApp.src.pyScripts.settings_friteuse import ManageFriteuse
from HaccpApp.haccpApp.src.pyScripts.settings_lieu import ManageLieu
from HaccpApp.haccpApp.src.pyScripts.settings_plan_nettoyage import ManagePlanNettoyage
from HaccpApp.haccpApp.src.pyScripts.operations_temperature_frigidaire import ManageTemperatureFridgeScreen


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


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(Button, Label):
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

        print(data_settings.keys())
        print(data_settings)

        collaborateur = ManageCollaborateurs(data=data_settings)
        collaborateur.load_operations()
        collaborateur.load_settings()

        element_refrigerant = ManageElementRefrigerant(data=data_settings)
        element_refrigerant.load_operations()
        element_refrigerant.load_settings()

        lieu = ManageLieu(data=data_settings)
        lieu.load_operations()
        lieu.load_settings()

        plan_nettoyage = ManagePlanNettoyage(data=data_settings)
        plan_nettoyage.load_operations()
        plan_nettoyage.load_settings()

        fournisseur = ManageFournisseurs(data=data_settings)
        fournisseur.load_operations()
        fournisseur.load_settings()

        categorie = ManageCategories(data=data_settings)
        categorie.load_operations()
        categorie.load_settings()

        friteuse = ManageFriteuse(data=data_settings)
        friteuse.load_operations()
        friteuse.load_settings()

        etiquette = ManageEtiquette(data=data_settings)
        etiquette.load_operations()
        etiquette.load_settings()

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
        # Get the screen manager from kv file
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition.direction = direction
        screen_manager.current = screen_name  # change current to the screen name I pass


MainApp().run()
