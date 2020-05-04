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

from pyScripts.utils import format_text, clean_widget


class LabelButton(ButtonBehavior, Label):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class ManageSettings:

    def __init__(self):
        self.app = App.get_running_app()
        self.root_ids = self.app.root.ids

        self.base_url = "https://haccpapp-40c63.firebaseio.com/{0}/settings/".format(self.app.local_id)

        self.settings_categorie = self.root_ids["settings_fournisseurs_screen"].ids
        self.settings_collaborateur = self.root_ids["settings_collaborateurs_screen"].ids
        self.settings_element_refrigerant = self.root_ids["settings_elements_refrigerants_screen"].ids
        self.settings_etiquette = self.root_ids["settings_etiquettes_screen"].ids
        self.settings_fournisseur = self.root_ids["settings_fournisseurs_screen"].ids
        self.settings_friteuse = self.root_ids["settings_friteuse_screen"].ids
        self.settings_plan_nettoyage_lieu = self.root_ids["settings_plan_nettoyage_screen"].ids
        self.settings_plan_nettoyage_element = self.root_ids["settings_plan_nettoyage_screen"].ids

        self.operations_etiquette = self.root_ids["operations_etiquette_screen"].ids
        self.operations_friteuse = self.root_ids["operations_friteuse_screen"].ids
        self.operations_plan_nettoyage = self.root_ids["operations_plan_nettoyage_screen"].ids
        self.operations_reception_produit = self.root_ids["operations_reception_produit_screen"].ids
        self.operations_temperature_frigidaire = self.root_ids["operations_temperature_frigo_screen"].ids
        self.operations_tracabilite = self.root_ids["operations_tracabilite_screen"].ids

    def get_data_settings(self, setting_name):

        if setting_name == 'collaborateur':
            text_input_nom = self.settings_collaborateur['settings_collaborateurs_nom']
            text_input_prenom = self.settings_collaborateur['settings_collaborateurs_prenom']

            nom = text_input_nom.text
            prenom = text_input_prenom.text

            if nom == "":
                text_input_nom.background_color = utils.get_color_from_hex("#C04A4A")
                return
            else:
                text_input_nom.background_color = [1, 1, 1, 1]

            if prenom == "":
                text_input_prenom.background_color = utils.get_color_from_hex("#C04A4A")
                return
            else:
                text_input_prenom.background_color = [1, 1, 1, 1]
        else:
            if setting_name == 'categorie':
                text_input = self.settings_categorie['settings_categorie_nom']
            elif setting_name == 'element_refrigerant':
                text_input = self.settings_element_refrigerant['settings_element_refrigerant_nom']
            elif setting_name == 'etiquette':
                text_input = self.settings_etiquette['settings_etiquette_nom']
            elif setting_name == 'fournisseur':
                text_input = self.settings_fournisseur['settings_fournisseurs_nom']
            elif setting_name == 'friteuse':
                text_input = self.settings_friteuse['settings_friteuse_nom']
            elif setting_name == 'plan_nettoyage_lieu':
                text_input = self.settings_plan_nettoyage_lieu['settings_lieu_nom']
            elif setting_name == 'plan_nettoyage_element':
                text_input = self.settings_plan_nettoyage_element['settings_plan_nettoyage_nom']
            else:
                print(setting_name)
                return

            nom = text_input.text

            if nom == "":
                text_input.background_color = utils.get_color_from_hex("#C04A4A")
                return
            else:
                text_input.background_color = [1, 1, 1, 1]

        if setting_name == 'collaborateur':
            self.query_firebase_add_data(nom=nom, prenom=prenom, setting_name=setting_name)
            text_input_nom.text = ""
            text_input_prenom.text = ""
        else:
            self.query_firebase_add_data(nom=nom, prenom=None, setting_name=setting_name)
            text_input.text = ""
        self.load_settings(setting_name=setting_name)
        self.load_operations(setting_name=setting_name)

    def delete_data(self, *args):
        id_ = args[0]
        setting_name = args[1]
        self.query_firebase_delete_data(id_=id_, setting_name=setting_name)
        self.load_settings(setting_name=setting_name)
        self.load_operations(setting_name=setting_name)

    def load_settings(self, data=None, setting_name=None):

        widget_dict = {'categorie': self.settings_categorie["settings_categorie_banner"],
                       'collaborateur': self.settings_collaborateur["settings_collaborateurs_screen_banner"],
                       'element_refrigerant': self.settings_element_refrigerant[
                           "settings_elements_refrigerants_screen_banner"],
                       'etiquette': self.settings_etiquette["settings_etiquette_screen_banner"],
                       'fournisseur': self.settings_fournisseur["settings_fournisseurs_banner"],
                       'friteuse': self.settings_friteuse["settings_friteuse_screen_banner"],
                       'plan_nettoyage_lieu': self.settings_plan_nettoyage_lieu["settings_lieu_screen_banner"],
                       'plan_nettoyage_element': self.settings_plan_nettoyage_element[
                           "settings_plan_nettoyage_screen_banner"]}

        if not setting_name:
            for k, v in widget_dict.items():
                v.clear_widgets()
                if data:
                    data_firebase = self.format_query_firebase(data=data, setting_name=k)
                else:
                    data_firebase = self.query_firebase_get_data(setting_name=k)

                self.load_settings_one_banner(widget=v, setting_name=k, data=data_firebase)

        else:
            widget = widget_dict[setting_name]
            widget.clear_widgets()
            if data:
                data_firebase = self.format_query_firebase(data=data, setting_name=setting_name)
            else:
                data_firebase = self.query_firebase_get_data(setting_name=setting_name)

            self.load_settings_one_banner(widget=widget, setting_name=setting_name, data=data_firebase)

    def load_settings_one_banner(self, widget, setting_name, data):

        if setting_name == "collaborateur":
            try:
                for response in data:
                    banner = BannerNomPrenomSettings(prenom=response['prenom'],
                                                     nom=response['nom'],
                                                     id=response['id'],
                                                     setting_name=setting_name)
                    widget.add_widget(banner)
            except Exception as e:
                print(setting_name + ' settings banner:', e, 'in', widget)
        else:
            try:
                for response in data:
                    banner = BannerNomSettings(nom=response['nom'],
                                               id=response['id'],
                                               setting_name=setting_name)
                    widget.add_widget(banner)
            except Exception as e:
                print(setting_name + ' settings banner:', e, 'in', widget)

    def load_operations(self, data=None, setting_name=None):

        widget_dic_categorie = [self.operations_reception_produit["reception_produit_selection_categorie_grid"]]

        widget_dic_collaborateur = [self.operations_temperature_frigidaire["temp_frigo_selection_collaborateur_grid"],
                                    self.operations_plan_nettoyage["plan_nettoyage_selection_collaborateur_grid"],
                                    self.operations_reception_produit["reception_produit_selection_collaborateur_grid"],
                                    self.operations_friteuse["friteuse_selection_collaborateur_grid"],
                                    self.operations_etiquette["etiquette_selection_collaborateur_grid"],
                                    self.operations_tracabilite["tracabilite_selection_collaborateur_grid"]]

        widget_dic_element_refrigerant = [self.operations_temperature_frigidaire["temp_frigo_selection_element_grid"]]

        widget_dic_etiquette = [self.operations_etiquette["etiquette_selection_produit_grid"]]

        widget_dic_fournisseur = [self.operations_reception_produit["reception_produit_selection_fournisseur_grid"]]

        widget_dic_friteuse = [self.operations_friteuse["friteuse_selection_friteuse_grid"]]

        widget_dic_lieu = [self.operations_plan_nettoyage["plan_nettoyage_selection_lieu_grid"]]

        widget_dic_plan_nettoyage = [self.operations_plan_nettoyage["plan_nettoyage_selection_plan_nettoyage"]]

        widget_dict = {'categorie': widget_dic_categorie,
                       'collaborateur': widget_dic_collaborateur,
                       'element_refrigerant': widget_dic_element_refrigerant,
                       'etiquette': widget_dic_etiquette,
                       'fournisseur': widget_dic_fournisseur,
                       'friteuse': widget_dic_friteuse,
                       'plan_nettoyage_lieu': widget_dic_lieu,
                       'plan_nettoyage_element': widget_dic_plan_nettoyage}

        if not setting_name:
            for k, v in widget_dict.items():
                for widget in v:
                    self.load_operations_one_banner(data=data, setting_name=k, widget=widget)
        else:
            for widget in widget_dict[setting_name]:
                self.load_operations_one_banner(data=data, setting_name=setting_name, widget=widget)

    def load_operations_one_banner(self, data, setting_name, widget):
        widget.clear_widgets()
        try:
            if data:
                response_list = self.format_query_firebase(data, setting_name)
            else:
                response_list = self.query_firebase_get_data(setting_name)
        except Exception as e:
            print(e)
            return
        if response_list:
            for response in response_list:
                try:
                    if setting_name == "collaborateur":
                        banner = BannerNomPrenom(nom=response['nom'],
                                                 prenom=response['prenom'],
                                                 banner=widget,
                                                 setting_name=setting_name)
                    else:
                        banner = BannerNom(nom=response['nom'],
                                           banner=widget,
                                           setting_name=setting_name)
                    widget.add_widget(banner)
                except Exception as e:
                    print(setting_name + ' banner:', e, 'in', widget)

    def query_firebase_get_data(self, setting_name):
        url = self.base_url + setting_name + ".json?auth={0}".format(self.app.id_token)
        response = requests.get(url=url)
        response_json = json.loads(response.content.decode())

        response_list = []

        if response_json:

            if setting_name == 'collaborateur':
                for k, v in response_json.items():
                    response_list.append({'nom': v['nom'], 'prenom': v['prenom'], 'id': k})
            else:
                for k, v in response_json.items():
                    response_list.append({'nom': v['nom'], 'id': k})

        return response_list

    def query_firebase_delete_data(self, id_, setting_name):
        url = self.base_url + setting_name + "/{0}.json?auth={1}".format(id_,  self.app.id_token)
        response = requests.delete(url=url)
        return json.dumps(response.content.decode())

    def query_firebase_add_data(self, nom, prenom, setting_name):

        if setting_name == 'collaborateur':
            data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"),
                    'prenom': format_text(prenom),
                    'nom': format_text(nom), 'id': str(uuid.uuid4())}
        else:
            data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"),
                    'nom': format_text(nom), 'id': str(uuid.uuid4())}

        url = self.base_url + setting_name + ".json"

        requests.post(url, data=json.dumps(data))

    def format_query_firebase(self, data, setting_name):
        response_list = []

        try:
            response_data = data[setting_name]
            if setting_name == 'collaborateur':
                for k, v in response_data.items():
                    response_list.append({'nom': v['nom'], 'prenom': v['prenom'], 'id': k})
            else:
                for k, v in response_data.items():
                    response_list.append({'nom': v['nom'], 'id': k})
        except Exception as e:
            print('error query db ', setting_name)
            return

        return response_list


class BannerNom(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(BannerNom, self).__init__()

        self.app = App.get_running_app()

        self.nom = kwargs.pop('nom')
        self.banner = kwargs.pop('banner')
        self.setting_name = kwargs.pop('setting_name')

        with self.canvas.before:
            Color(rgba=(utils.get_color_from_hex("#0062D1")))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Left floatlayout
        left_fl = FloatLayout()
        left_fl_title = LabelButton(text=self.nom, size_hint=(1, 1), pos_hint={"top": 1, "right": 1},
                                    color=utils.get_color_from_hex("#ffffff"),
                                    on_release=partial(self.select_element, self.banner, self.setting_name))

        left_fl.add_widget(left_fl_title)

        self.add_widget(left_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def select_element(self, *args):
        print(args)
        banner = args[0]
        setting_name = args[1]
        widget = args[2]
        clean_widget(banner)
        widget.color = utils.get_color_from_hex("#35477d")
        if setting_name == 'categorie':
            self.app.categorie_choice = widget.text
        elif setting_name == 'element_refrigerant':
            self.app.element_refrigerant_choice = widget.text
        elif setting_name == 'etiquette':
            self.app.etiquette_choice = widget.text
        elif setting_name == 'fournisseur':
            self.app.fournisseur_choice = widget.text
        elif setting_name == 'plan_nettoyage_lieu':
            self.app.lieu_choice = widget.text
        elif setting_name == 'plan_nettoyage_element':
            self.app.plan_nettoyage_choice = widget.text
        elif setting_name == 'friteuse':
            self.app.friteuse_choice = widget.text
        else:
            print(setting_name)


class BannerNomPrenom(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(BannerNomPrenom, self).__init__()

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


class BannerNomSettings(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(BannerNomSettings, self).__init__()

        self.nom = kwargs.pop('nom')
        self.id = kwargs.pop('id')
        self.setting_name = kwargs.pop('setting_name')

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
                                      on_release=partial(ManageSettings().delete_data, self.id, self.setting_name))
        right_fl.add_widget(right_fl_delete)

        self.add_widget(left_fl)
        self.add_widget(right_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class BannerNomPrenomSettings(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(BannerNomPrenomSettings, self).__init__()

        self.nom = kwargs.pop('prenom') + " " + kwargs.pop('nom')
        self.id = kwargs.pop('id')
        self.setting_name = kwargs.pop('setting_name')

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
                                      on_release=partial(ManageSettings().delete_data, self.id, self.setting_name))
        right_fl.add_widget(right_fl_delete)

        self.add_widget(left_fl)
        self.add_widget(right_fl)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
