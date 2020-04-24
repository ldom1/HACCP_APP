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


class ManageCollaborateurs:

    def __init__(self):
        self.app = App.get_running_app()
        self.settings = self.app.root.ids["settings_collaborateurs_screen"]
        self.settings_data = self.settings.ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/test_user/settings/collaborateur"

    def get_data_settings(self):
        nom = self.settings_data['settings_collaborateurs_nom'].text
        prenom = self.settings_data['settings_collaborateurs_prenom'].text

        if nom == "":
            self.settings_data['settings_collaborateurs_nom'].background_color = utils.get_color_from_hex(
                "#C04A4A")
            return
        else:
            self.settings_data['settings_collaborateurs_nom'].background_color = [1, 1, 1, 1]

        if prenom == "":
            self.settings_data[
                'settings_collaborateurs_prenom'].background_color = utils.get_color_from_hex("#C04A4A")
            return
        else:
            self.settings_data['settings_collaborateurs_prenom'].background_color = [1, 1, 1, 1]

        self.query_firebase_add_data(nom=nom, prenom=prenom)
        self.settings_data['settings_collaborateurs_nom'].text = ""
        self.settings_data['settings_collaborateurs_prenom'].text = ""
        self.load_settings()
        self.load_operations()

    def delete_data(self, *args):
        id = args[0]
        self.query_firebase_delete_data(id)
        self.load_settings()
        self.load_operations()

    def load_settings(self, data=None):
        self.settings_data["settings_collaborateurs_screen_banner"].clear_widgets()
        if data:
            data_firebase = self.format_query_firebase(data=data)
        else:
            data_firebase = self.query_firebase_get_data()
        try:
            for response in data_firebase:
                banner = CollaborateursBannerSettings(prenom=response['prenom'],
                                                      nom=response['nom'],
                                                      id=response['id'])
                self.settings_data["settings_collaborateurs_screen_banner"].add_widget(banner)
        except Exception as e:
            print('Settings collaborateurs banner:', e)

    def load_operations(self, data=None):
        widget_dict = [
            self.app.root.ids["operations_temperature_frigo_screen"].ids["temp_frigo_selection_collaborateur_grid"],
            self.app.root.ids["operations_plan_nettoyage_screen"].ids["plan_nettoyage_selection_collaborateur_grid"],
            self.app.root.ids["operations_reception_produit_screen"].ids[
                "reception_produit_selection_collaborateur_grid"],
            self.app.root.ids["operations_friteuse_screen"].ids["friteuse_selection_collaborateur_grid"],
            self.app.root.ids["operations_etiquette_screen"].ids["etiquette_selection_collaborateur_grid"],
            self.app.root.ids["operations_tracabilite_screen"].ids["tracabilite_selection_collaborateur_grid"]]
        for widget in widget_dict:
            self.load_operations_one_banner(data=data, widget=widget)

    def load_operations_one_banner(self, data, widget):
        widget.clear_widgets()
        try:
            if data:
                response_list = self.format_query_firebase(data=data)
            else:
                response_list = self.query_firebase_get_data()
        except Exception as e:
            print(e)
            return
        for response in response_list:
            try:
                banner = CollaborateursBanner(prenom=response['prenom'],
                                              nom=response['nom'],
                                              banner=widget)
                widget.add_widget(banner)
            except Exception as e:
                print('Collaborateurs banner:', e, 'in', widget)

    def query_firebase_get_data(self):
        url = self.base_url + ".json"
        response = requests.get(url=url)
        response_json = json.loads(response.content.decode())

        response_list = []

        for k, v in response_json.items():
            response_list.append({'nom': v['nom'], 'prenom': v['prenom'], 'id': k})

        return response_list

    def query_firebase_delete_data(self, id):
        url = self.base_url + "/{0}.json".format(id)
        response = requests.delete(url=url)
        return json.dumps(response.content.decode())

    def query_firebase_add_data(self, nom, prenom):
        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"),
                'prenom': format_text(prenom),
                'nom': format_text(nom), 'id': str(uuid.uuid4())}

        url = self.base_url + ".json"

        requests.post(url, data=json.dumps(data))

    def format_query_firebase(self, data):
        response_list = []

        for k, v in data['collaborateur'].items():
            response_list.append({'nom': v['nom'], 'prenom': v['prenom'], 'id': k})

        return response_list


class CollaborateursBanner(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(CollaborateursBanner, self).__init__()

        self.app = App.get_running_app()

        self.nom = kwargs.pop('prenom') + " " + kwargs.pop('nom')
        self.banner = kwargs.pop('banner')

        with self.canvas.before:
            Color(rgba=(utils.get_color_from_hex("#0062D1")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Left floatlayout
        left_fl = FloatLayout()
        left_fl_title = LabelButton(text=self.nom, size_hint=(1, 1), pos_hint={"top": 1, "right": 1},
                                    color=utils.get_color_from_hex("#ffffff"),
                                    on_release=partial(self.select_element, self.banner))

        left_fl.add_widget(left_fl_title)

        self.add_widget(left_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def select_element(self, *args):
        widget = args[1]
        banner = args[0]
        clean_widget(widget=banner)
        widget.color = utils.get_color_from_hex("#35477d")
        self.app.collaborateur_choice = widget.text


class CollaborateursBannerSettings(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(CollaborateursBannerSettings, self).__init__()

        self.nom = kwargs.pop('prenom') + " " + kwargs.pop('nom')
        self.id = kwargs.pop('id')

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
                                      on_release=partial(ManageCollaborateurs().delete_data, self.id))
        right_fl.add_widget(right_fl_delete)

        self.add_widget(left_fl)
        self.add_widget(right_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
