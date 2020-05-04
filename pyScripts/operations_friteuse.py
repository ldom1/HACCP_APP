# Temperature Fridge
import datetime
import json
import uuid

from kivy.app import App

import requests

from pyScripts.utils import clean_widget


class ManageFriteuseScreen:

    def __init__(self):

        self.app = App.get_running_app()
        self.screen_data = self.app.root.ids['operations_friteuse_screen'].ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/{0}/operations/friteuse.json?auth={1}".format(
            self.app.local_id,
            self.app.id_token)

    def get_data(self):

        try:
            friteuse_choice = self.app.friteuse_choice
            if not friteuse_choice:
                self.screen_data['warning'].text = "Veuillez sélectionner une friteuse"
                return
        except Exception as e:
            print(e)
            self.screen_data['warning'].text = "Veuillez sélectionner une friteuse"
            return
        try:
            qualite_huile_choice = self.app.qualite_huile_choice
            if not qualite_huile_choice:
                self.screen_data['warning'].text = "Veuillez sélectionner oui/non pour la qualité de l'huile"
                return
        except Exception as e:
            print(e)
            self.screen_data['warning'].text = "Veuillez sélectionner oui/non pour la qualité de l'huile"
            return

        try:
            remplacement_huile_choice = self.app.remplacement_huile_choice
            if not remplacement_huile_choice:
                self.screen_data['warning'].text = "Veuillez sélectionner oui/non pour le remplacement de l'huile"
                return
        except Exception as e:
            print(e)
            self.screen_data['warning'].text = "Veuillez sélectionner oui/non pour le remplacement de l'huile"
            return

        try:
            collaborateur_choice = self.app.collaborateur_choice
            if not collaborateur_choice:
                self.screen_data['warning'].text = "Veuillez sélectionner un collaborateur"
                return
        except Exception as e:
            print(e)
            self.screen_data['warning'].text = "Veuillez sélectionner un collaborateur"
            return

        self.screen_data['warning'].text = ""

        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"), 'friteuse': friteuse_choice,
                'qualite_huile': qualite_huile_choice, 'remplacement_huile': remplacement_huile_choice,
                'collaborateur': collaborateur_choice,
                'id': str(uuid.uuid4())}

        response = requests.post(self.base_url, data=json.dumps(data))
        print(response.content.decode())

        self.app.change_screen(screen_name='home_screen', direction='right')
        self.app.lieu_choice = None
        self.app.plan_nettoyage_choice = None
        self.app.collaborateur_choice = None

    def clear_screen(self):
        clean_widget(self.screen_data["friteuse_selection_friteuse_grid"])
        clean_widget(self.screen_data["friteuse_selection_collaborateur_grid"])
