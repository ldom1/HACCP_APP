from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy import utils

from HaccpApp.haccpApp.src.pyScripts.collaborateurs import ManageCollaborateurs
from HaccpApp.haccpApp.src.pyScripts.elements_refrigerants import ManageElementRefrigerant
from HaccpApp.haccpApp.src.pyScripts.plan_nettoyage import ManagePlanNettoyageElement, ManagePlanNettoyageLieu
from HaccpApp.haccpApp.src.pyScripts.temperature_fridge_script import ManageTemperatureFridgeScreen


class HomeScreen(Screen):
    pass


class TemperatureFrigoScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class SettingsCollaborateursScreen(Screen):
    pass


class SettingsElementsRefrigerantsScreen(Screen):
    pass


class SettingsPlanNettoyageScreen(Screen):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


GUI = Builder.load_file("main.kv")


class MainApp(App):
    def build(self):
        return GUI

    def on_start(self):
        ManageCollaborateurs().load_collaborateurs()
        ManageCollaborateurs().load_collaborateurs_settings()

        ManageElementRefrigerant().load_elements_refrigerants()
        ManageElementRefrigerant().load_elements_refrigerants_settings()

        # ManagePlanNettoyageLieu().load_()
        ManagePlanNettoyageLieu().load_plan_nettoyage_lieu_settings()

        # ManagePlanNettoyageElement().load_()
        ManagePlanNettoyageElement().load_plan_nettoyage_element_settings()

    def change_screen(self, screen_name, direction):
        # Clean selected screen
        if screen_name == "temperature_frigo_screen":
            ManageTemperatureFridgeScreen().clear_temperature_fridge_screen()
        # Get the screen manager from kv file
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition.direction = direction
        screen_manager.current = screen_name  # change current to the screen name I pass


MainApp().run()
