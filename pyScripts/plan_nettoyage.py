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
            plan_nettoyage_lieu_list = self.query_firebase_get_plan_nettoyage_lieu()
            for plan_nettoyage_lieu in plan_nettoyage_lieu_list:
                settings_plan_nettoyage_banner = PlanNettoyageLieuBannerSettings(nom=plan_nettoyage_lieu['nom'],
                                                                                 plan_nettoyage_lieu_id=
                                                                                 plan_nettoyage_lieu['id'])
                self.settings_plan_net_lieu_data["settings_plan_nettoyage_lieu_screen_banner"].add_widget(
                    settings_plan_nettoyage_banner)
        except Exception as e:
            print('Settings Plan nettoyage lieu banner:', e)

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


class ManagePlanNettoyageElement:

    def __init__(self):
        self.app = App.get_running_app()
        self.settings_plan_net_element = self.app.root.ids["settings_plan_nettoyage_screen"]
        self.settings_plan_net_element_data = self.settings_plan_net_element.ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/test_user/settings/plan_nettoyage_element"

    def get_data_settings_plan_nettoyage_element(self):
        nom_plan_nettoyage_elt = self.settings_plan_net_element_data['settings_plan_nettoyage_element_nom'].text

        if nom_plan_nettoyage_elt == "":
            self.settings_plan_net_element_data[
                'settings_plan_nettoyage_element_nom'].background_color = utils.get_color_from_hex(
                "#C04A4A")
            return
        else:
            self.settings_plan_net_element_data['settings_plan_nettoyage_element_nom'].background_color = [1, 1, 1, 1]

        self.query_firebase_add_plan_nettoyage_element(nom_plan_nettoyage_element=nom_plan_nettoyage_elt)
        self.settings_plan_net_element_data['settings_plan_nettoyage_element_nom'].text = ""
        self.load_plan_nettoyage_element_settings()
        self.load_plan_nettoyage_element()

    def delete_plan_nettoyage_element(self, *args):
        plan_nettoyage_element_id = args[0]
        self.query_firebase_delete_plan_nettoyage_element(plan_nettoyage_element_id)
        self.load_plan_nettoyage_element_settings()
        self.load_plan_nettoyage_element()

    def load_plan_nettoyage_element_settings(self):
        self.settings_plan_net_element_data["settings_plan_nettoyage_element_screen_banner"].clear_widgets()
        try:
            plan_nettoyage_element_list = self.query_firebase_get_plan_nettoyage_element()
            for plan_nettoyage_element in plan_nettoyage_element_list:
                settings_plan_nettoyage_element_banner = PlanNettoyageElementBannerSettings(
                    nom=plan_nettoyage_element['nom'],
                    plan_nettoyage_element_id=plan_nettoyage_element['id'])
                self.settings_plan_net_element_data["settings_plan_nettoyage_element_screen_banner"].add_widget(
                    settings_plan_nettoyage_element_banner)
        except Exception as e:
            print('Settings Plan nettoyage element banner:', e)

    def load_plan_nettoyage_element(self):
        print('to do')

    def query_firebase_get_plan_nettoyage_element(self):
        url = self.base_url + ".json"
        response = requests.get(url=url)
        plan_nettoyage_element_json = json.loads(response.content.decode())

        plan_nettoyage_element_list = []

        for k, v in plan_nettoyage_element_json.items():
            plan_nettoyage_element_list.append({'nom': v['nom'], 'id': k})

        return plan_nettoyage_element_list

    def query_firebase_delete_plan_nettoyage_element(self, id):
        url = self.base_url + "/{0}.json".format(id)
        response = requests.delete(url=url)
        return json.dumps(response.content.decode())

    def query_firebase_add_plan_nettoyage_element(self, nom_plan_nettoyage_element):
        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"),
                'nom': format_text(nom_plan_nettoyage_element), 'id': str(uuid.uuid4())}

        url = self.base_url + ".json"

        requests.post(url, data=json.dumps(data))


class PlanNettoyageElementBanner(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(PlanNettoyageElementBanner, self).__init__()

        self.app = App.get_running_app()

        self.nom = kwargs.pop('nom')

        with self.canvas.before:
            Color(rgba=(utils.get_color_from_hex("#0062D1")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Left floatlayout
        left_fl = FloatLayout()
        left_fl_title = LabelButton(text=self.nom, size_hint=(1, 1), pos_hint={"top": 1, "right": 1},
                                    color=utils.get_color_from_hex("#ffffff"),
                                    on_release=partial(self.select_plan_nettoyage_element, self.app))

        left_fl.add_widget(left_fl_title)

        self.add_widget(left_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def select_plan_nettoyage_element(self, *args):
        clean_widget(app=self.app, screen_id="temperature_frigo_screen",
                     widget_id="temp_frigo_selection_collaborateur_grid")
        running_app = args[0]
        widget = args[1]
        widget.color = utils.get_color_from_hex("#35477d")
        running_app.collaborateur_choice = widget.text


class PlanNettoyageElementBannerSettings(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        app = App.get_running_app()
        super(PlanNettoyageElementBannerSettings, self).__init__()

        self.nom = kwargs.pop('nom')
        self.plan_nettoyage_element_id = kwargs.pop('plan_nettoyage_element_id')

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
                                      on_release=partial(ManagePlanNettoyageElement().delete_plan_nettoyage_element,
                                                         self.plan_nettoyage_element_id))
        right_fl.add_widget(right_fl_delete)

        self.add_widget(left_fl)
        self.add_widget(right_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
