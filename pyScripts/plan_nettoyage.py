import datetime
import json
import uuid

import requests
from kivy import utils
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.button import ButtonBehavior
from kivy.app import App
from functools import partial

from HaccpApp.haccpApp.src.pyScripts.utils import format_text, clean_widget


class LabelButton(ButtonBehavior, Label):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class ManagePlanNettoyageLieu:

    def __init__(self):
        self.app = App.get_running_app()
        self.settings_plan_net_lieu = self.app.root.ids["settings_plan_nettoyage_screen"]
        self.settings_plan_net_lieu_data = self.settings_plan_net_lieu.ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/test_user/settings/plan_nettoyage_lieu"

    def get_data_settings_plan_nettoyage_lieu(self):
        nom_plan_nettoyage_lieu = self.settings_plan_net_lieu_data['settings_plan_nettoyage_lieu_nom'].text

        if nom_plan_nettoyage_lieu == "":
            self.settings_plan_net_lieu_data[
                'settings_plan_nettoyage_lieu_nom'].background_color = utils.get_color_from_hex(
                "#C04A4A")
            return
        else:
            self.settings_plan_net_lieu_data['settings_plan_nettoyage_lieu_nom'].background_color = [1, 1, 1, 1]

        self.query_firebase_add_plan_nettoyage_lieu(nom_plan_nettoyage_lieu=nom_plan_nettoyage_lieu)
        self.settings_plan_net_lieu_data['settings_plan_nettoyage_lieu_nom'].text = ""
        self.load_plan_nettoyage_lieu_settings()
        self.load_plan_nettoyage_lieu()

    def delete_plan_nettoyage_lieu(self, *args):
        plan_nettoyage_lieu_id = args[0]
        self.query_firebase_delete_plan_nettoyage_lieu(plan_nettoyage_lieu_id)
        self.load_plan_nettoyage_lieu_settings()
        self.load_plan_nettoyage_lieu()

    def load_plan_nettoyage_lieu_settings(self):
        self.settings_plan_net_lieu_data["settings_plan_nettoyage_lieu_screen_banner"].clear_widgets()
        try:
            collaborateurs_list = self.query_firebase_get_plan_nettoyage_lieu()
            for collaborateur in collaborateurs_list:
                settings_collaborateur_banner = PlanNettoyageLieuBannerSettings(nom=collaborateur['nom'],
                                                                                plan_nettoyage_lieu_id=collaborateur[
                                                                                    'id'])
                self.settings_plan_net_lieu_data["settings_plan_nettoyage_lieu_screen_banner"].add_widget(
                    settings_collaborateur_banner)
        except Exception as e:
            print('Settings collaborateurs banner:', e)

    def load_plan_nettoyage_lieu(self):
        print('to do')

    def query_firebase_get_plan_nettoyage_lieu(self):
        url = self.base_url + ".json"
        response = requests.get(url=url)
        plan_nettoyage_lieu_json = json.loads(response.content.decode())

        plan_nettoyage_lieu_list = []

        for k, v in plan_nettoyage_lieu_json.items():
            plan_nettoyage_lieu_list.append({'nom': v['nom'], 'id': k})

        return plan_nettoyage_lieu_list

    def query_firebase_delete_plan_nettoyage_lieu(self, id):
        url = self.base_url + "/{0}.json".format(id)
        response = requests.delete(url=url)
        return json.dumps(response.content.decode())

    def query_firebase_add_plan_nettoyage_lieu(self, nom_plan_nettoyage_lieu):
        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"),
                'nom': format_text(nom_plan_nettoyage_lieu), 'id': str(uuid.uuid4())}

        url = self.base_url + ".json"

        requests.post(url, data=json.dumps(data))


class PlanNettoyageLieuBanner(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(PlanNettoyageLieuBanner, self).__init__()

        self.app = App.get_running_app()

        self.nom = kwargs.pop('prenom') + " " + kwargs.pop('nom')

        with self.canvas.before:
            Color(rgba=(utils.get_color_from_hex("#0062D1")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Left floatlayout
        left_fl = FloatLayout()
        left_fl_title = LabelButton(text=self.nom, size_hint=(1, 1), pos_hint={"top": 1, "right": 1},
                                    color=utils.get_color_from_hex("#ffffff"),
                                    on_release=partial(self.select_plan_nettoyage_lieu, self.app))

        left_fl.add_widget(left_fl_title)

        self.add_widget(left_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def select_plan_nettoyage_lieu(self, *args):
        clean_widget(app=self.app, screen_id="temperature_frigo_screen",
                     widget_id="temp_frigo_selection_collaborateur_grid")
        running_app = args[0]
        widget = args[1]
        widget.color = utils.get_color_from_hex("#35477d")
        running_app.collaborateur_choice = widget.text


class PlanNettoyageLieuBannerSettings(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        app = App.get_running_app()
        super(PlanNettoyageLieuBannerSettings, self).__init__()

        self.nom = kwargs.pop('nom')
        self.plan_nettoyage_lieu_id = kwargs.pop('plan_nettoyage_lieu_id')

        with self.canvas.before:
            Color(rgba=(utils.get_color_from_hex("#0062D1")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Left floatlayout
        left_fl = FloatLayout()
        left_fl_title = LabelButton(text=self.nom, size_hint=(.9, 1), pos_hint={"top": 1, "right": 1},
                                    color=utils.get_color_from_hex("#ffffff"))

        left_fl.add_widget(left_fl_title)

        # right floatlayout - Bouton delete
        right_fl = FloatLayout()
        right_fl_delete = ImageButton(source="icons/delete.png", size_hint=(.4, .4), pos_hint={"top": .7, "right": 1},
                                      on_release=partial(ManagePlanNettoyageLieu().delete_plan_nettoyage_lieu,
                                                         self.plan_nettoyage_lieu_id))
        right_fl.add_widget(right_fl_delete)

        self.add_widget(left_fl)
        self.add_widget(right_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class ManagePlanNettoyageElements:

    def __init__(self):
        self.app = App.get_running_app()
        self.settings_collaborateur = self.app.root.ids["settings_collaborateurs_screen"]
        self.settings_collaborateur_data = self.settings_collaborateur.ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/test_user/settings/collaborateurs"

    def get_data_settings_collaborateurs(self):
        nom_collaborateur = self.settings_collaborateur_data['settings_collaborateurs_nom'].text
        prenom_collaborateur = self.settings_collaborateur_data['settings_collaborateurs_prenom'].text

        if nom_collaborateur == "":
            self.settings_collaborateur_data['settings_collaborateurs_nom'].background_color = utils.get_color_from_hex(
                "#C04A4A")
            return
        else:
            self.settings_collaborateur_data['settings_collaborateurs_nom'].background_color = [1, 1, 1, 1]

        if prenom_collaborateur == "":
            self.settings_collaborateur_data[
                'settings_collaborateurs_prenom'].background_color = utils.get_color_from_hex("#C04A4A")
            return
        else:
            self.settings_collaborateur_data['settings_collaborateurs_prenom'].background_color = [1, 1, 1, 1]

        self.query_firebase_add_collaborateur(nom_collaborateur=nom_collaborateur,
                                              prenom_collaborateur=prenom_collaborateur)
        self.settings_collaborateur_data['settings_collaborateurs_nom'].text = ""
        self.settings_collaborateur_data['settings_collaborateurs_prenom'].text = ""
        self.load_collaborateurs_settings()
        self.load_collaborateurs()

    def delete_collaborateur(self, *args):
        collaborateur_id = args[0]
        self.query_firebase_delete_collaborateur(collaborateur_id)
        self.load_collaborateurs_settings()
        self.load_collaborateurs()

    def load_collaborateurs_settings(self):
        self.settings_collaborateur_data["settings_collaborateurs_screen_banner"].clear_widgets()
        try:
            collaborateurs_list = self.query_firebase_get_collaborateur()
            for collaborateur in collaborateurs_list:
                settings_collaborateur_banner = CollaborateursBannerSettings(prenom=collaborateur['prenom'],
                                                                             nom=collaborateur['nom'],
                                                                             collaborateur_id=collaborateur['id'])
                self.settings_collaborateur_data["settings_collaborateurs_screen_banner"].add_widget(
                    settings_collaborateur_banner)
        except Exception as e:
            print('Settings collaborateurs banner:', e)

    def load_collaborateurs(self):
        self.app.root.ids["temperature_frigo_screen"].ids["temp_frigo_selection_collaborateur_grid"].clear_widgets()
        # Temp Frigo
        try:
            collaborateurs_list = self.query_firebase_get_collaborateur()
        except Exception as e:
            print(e)
            return
        for collaborateur in collaborateurs_list:
            try:
                settings_collaborateur_banner = CollaborateursBanner(prenom=collaborateur['prenom'],
                                                                     nom=collaborateur['nom'])
                self.app.root.ids["temperature_frigo_screen"].ids["temp_frigo_selection_collaborateur_grid"].add_widget(
                    settings_collaborateur_banner)
            except Exception as e:
                print('Collaborateurs Temp Frigo banner:', e)

    def query_firebase_get_collaborateur(self):
        url = self.base_url + ".json"
        response = requests.get(url=url)
        collaborateur_json = json.loads(response.content.decode())

        collaborateur_list = []

        for k, v in collaborateur_json.items():
            collaborateur_list.append({'nom': v['nom'], 'prenom': v['prenom'], 'id': k})

        return collaborateur_list

    def query_firebase_delete_collaborateur(self, id):
        url = self.base_url + "/{0}.json".format(id)
        response = requests.delete(url=url)
        return json.dumps(response.content.decode())

    def query_firebase_add_collaborateur(self, nom_collaborateur, prenom_collaborateur):
        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"),
                'prenom': format_text(prenom_collaborateur),
                'nom': format_text(nom_collaborateur), 'id': str(uuid.uuid4())}

        url = self.base_url + ".json"

        requests.post(url, data=json.dumps(data))
