from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior, Button
from kivy.uix.image import Image

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

    def on_start(self):
        ManageCollaborateurs().load_operations()
        ManageCollaborateurs().load_settings()

        ManageElementRefrigerant().load_operations()
        ManageElementRefrigerant().load_settings()

        ManageLieu().load_operations()
        ManageLieu().load_settings()

        ManagePlanNettoyage().load_operations()
        ManagePlanNettoyage().load_settings()

        ManageFournisseurs().load_operations()
        ManageFournisseurs().load_settings()

        ManageCategories().load_operations()
        ManageCategories().load_settings()

        ManageFriteuse().load_operations()
        ManageFriteuse().load_settings()

        # ManageEtiquette().load_()
        ManageEtiquette().load_settings()

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
        # Get the screen manager from kv file
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition.direction = direction
        screen_manager.current = screen_name  # change current to the screen name I pass


MainApp().run()
