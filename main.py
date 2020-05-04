#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time

import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

from pyScripts.operations_etiquette import ManageEtiquetteScreen
from pyScripts.operations_friteuse import ManageFriteuseScreen
from pyScripts.operations_plan_nettoyage import ManagePlanNettoyageScreen
from pyScripts.operations_reception_produit import ManageReceptionProduitScreen
from pyScripts.operations_tracabilite import ManageTracabiliteScreen
from pyScripts.operations_temperature_frigidaire import ManageTemperatureFridgeScreen

from pyScripts.login import Login
from pyScripts.settings import ManageSettings


class HomeScreen(Screen):
    pass


class LoginScreen(Screen):
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


class LabelButton(ButtonBehavior, Label):
    pass


class CameraClick(BoxLayout):
    pass


GUI = Builder.load_file("main.kv")


class MainApp(App):
    refresh_token_file = "refresh_token.txt"

    def build(self):

        self.login = Login()

        return GUI

    def load_data(self, local_id, id_token):
        start_time = time.time()
        url_settings = "https://haccpapp-40c63.firebaseio.com/{0}/settings/.json?auth={1}".format(local_id,
                                                                                                  id_token)
        response = requests.get(url=url_settings)
        data_settings = json.loads(response.content.decode())
        print('First query executed in:', time.time() - start_time, 's')
        return data_settings

    def on_start(self):

        try:
            with open(self.refresh_token_file, 'r') as f:
                refresh_token = f.read()
            f.close()

            # Use refresh token to get a new idToken
            id_token, local_id = self.login.exchange_refresh_token(refresh_token)

            self.id_token = id_token
            self.local_id = local_id

            print('Id token:', id_token)
            print('Local Id token:', local_id)

            data_settings = self.load_data(local_id=local_id, id_token=id_token)

            start_time = time.time()
            self.settings = ManageSettings()
            self.settings.load_operations(data=data_settings)
            self.settings.load_settings(data=data_settings)

            print('Settings loaded in', time.time() - start_time, 's')

            self.change_screen(screen_name="home_screen", direction="left")

        except Exception as e:
            print(e)

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
