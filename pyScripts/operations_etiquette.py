# Temperature Fridge
import datetime
import json
import uuid

from kivy.app import App

import requests

from HaccpApp.haccpApp.src.pyScripts.utils import clean_widget


class ManageEtiquetteScreen:

    def __init__(self):

        self.app = App.get_running_app()
        self.screen_data = self.app.root.ids['operations_etiquette_screen'].ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/test_user/operations/etiquette.json"

    def get_data(self):

        try:
            etiquette_choice = self.app.etiquette_choice
            if not etiquette_choice:
                self.screen_data['warning'].text = "Veuillez sélectionner un produit"
                return
        except Exception as e:
            print(e)
            self.screen_data['warning'].text = "Veuillez sélectionner un produit"
            return
        try:
            dlc_choice = self.app.dlc_choice
            if not dlc_choice:
                self.screen_data['warning'].text = "Veuillez sélectionner un DLC"
                return
        except Exception as e:
            print(e)
            self.screen_data['warning'].text = "Veuillez sélectionner un DLC"
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

        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"),
                'etiquette': etiquette_choice, 'DLC': dlc_choice,
                'collaborateur': collaborateur_choice,
                'id': str(uuid.uuid4())}

        response = requests.post(self.base_url, data=json.dumps(data))
        print(response.content.decode())

        self.app.change_screen(screen_name='home_screen', direction='right')
        self.app.lieu_choice = None
        self.app.plan_nettoyage_choice = None
        self.app.collaborateur_choice = None

    def clear_screen(self):
        clean_widget(self.screen_data["etiquette_selection_produit_grid"])
        clean_widget(self.screen_data["etiquette_selection_collaborateur_grid"])
