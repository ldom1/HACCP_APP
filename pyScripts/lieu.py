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


class ManageLieu:

    def __init__(self):
        self.app = App.get_running_app()
        self.settings_plan_net_lieu = self.app.root.ids["settings_plan_nettoyage_screen"]
        self.settings_plan_net_lieu_data = self.settings_plan_net_lieu.ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/test_user/settings/plan_nettoyage_lieu"

    def get_data_settings(self):
        nom = self.settings_plan_net_lieu_data['settings_lieu_nom'].text

        if nom == "":
            self.settings_plan_net_lieu_data[
                'settings_lieu_nom'].background_color = utils.get_color_from_hex(
                "#C04A4A")
            return
        else:
            self.settings_plan_net_lieu_data['settings_lieu_nom'].background_color = [1, 1, 1, 1]

        self.query_firebase_add_data(nom=nom)
        self.settings_plan_net_lieu_data['settings_lieu_nom'].text = ""
        self.load_lieu_settings()
        self.load_lieu()

    def delete_data(self, *args):
        plan_nettoyage_lieu_id = args[0]
        self.query_firebase_delete_data(plan_nettoyage_lieu_id)
        self.load_lieu_settings()
        self.load_lieu()

    def load_lieu_settings(self):
        self.settings_plan_net_lieu_data["settings_lieu_screen_banner"].clear_widgets()
        try:
            response_list = self.query_firebase_get_data()
            for response in response_list:
                settings_lieu_banner = LieuBannerSettings(nom=response['nom'], id=response['id'])
                self.settings_plan_net_lieu_data["settings_lieu_screen_banner"].add_widget(
                    settings_lieu_banner)
        except Exception as e:
            print('Settings Plan nettoyage lieu banner:', e)

    def load_lieu(self):
        print('to do')

    def query_firebase_get_data(self):
        url = self.base_url + ".json"
        response = requests.get(url=url)
        response_json = json.loads(response.content.decode())

        response_list = []

        for k, v in response_json.items():
            response_list.append({'nom': v['nom'], 'id': k})

        return response_list

    def query_firebase_delete_data(self, id):
        url = self.base_url + "/{0}.json".format(id)
        response = requests.delete(url=url)
        return json.dumps(response.content.decode())

    def query_firebase_add_data(self, nom):
        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"),
                'nom': format_text(nom), 'id': str(uuid.uuid4())}

        url = self.base_url + ".json"

        requests.post(url, data=json.dumps(data))


class LieuBanner(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(LieuBanner, self).__init__()

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
                                    on_release=partial(self.select_element, self.app))

        left_fl.add_widget(left_fl_title)

        self.add_widget(left_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def select_element(self, *args):
        clean_widget(app=self.app, screen_id="temperature_frigo_screen",
                     widget_id="temp_frigo_selection_collaborateur_grid")
        running_app = args[0]
        widget = args[1]
        widget.color = utils.get_color_from_hex("#35477d")
        running_app.collaborateur_choice = widget.text


class LieuBannerSettings(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(LieuBannerSettings, self).__init__()

        self.nom = kwargs.pop('nom')
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
                                      on_release=partial(ManageLieu().delete_data, self.id))
        right_fl.add_widget(right_fl_delete)

        self.add_widget(left_fl)
        self.add_widget(right_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
