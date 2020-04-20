# Temperature Fridge
import datetime
import json
import uuid

from kivy.app import App

import requests

from HaccpApp.haccpApp.src.pyScripts.utils import clean_widget


class ManagePlanNettoyageScreen:

    def __init__(self):

        self.app = App.get_running_app()
        self.plan_nettoyage_data = self.app.root.ids['operations_plan_nettoyage_screen'].ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/test_user/operations/plan_nettoyage.json"

    def get_data(self):

        try:
            lieu_choice = self.app.lieu_choice
            if not lieu_choice:
                self.plan_nettoyage_data['warning'].text = "Veuillez sélectionner un lieu"
                return
        except Exception as e:
            print(e)
            self.plan_nettoyage_data['warning'].text = "Veuillez sélectionner un lieu"
            return
        try:
            plan_nettoyage_choice = self.app.plan_nettoyage_choice
            if not plan_nettoyage_choice:
                self.plan_nettoyage_data['warning'].text = "Veuillez sélectionner un élément à nettoyer"
                return
        except Exception as e:
            print(e)
            self.plan_nettoyage_data['warning'].text = "Veuillez sélectionner un élément à nettoyer"
            return

        try:
            collaborateur_choice = self.app.collaborateur_choice
            if not collaborateur_choice:
                self.plan_nettoyage_data['warning'].text = "Veuillez sélectionner un collaborateur"
                return
        except Exception as e:
            print(e)
            self.plan_nettoyage_data['warning'].text = "Veuillez sélectionner un collaborateur"
            return

        self.plan_nettoyage_data['warning'].text = ""

        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"), 'lieu': lieu_choice,
                'plan_nettoyage': plan_nettoyage_choice, 'collaborateur': collaborateur_choice,
                'id': str(uuid.uuid4())}

        response = requests.post(self.base_url, data=json.dumps(data))
        print(response.content.decode())

        self.app.change_screen(screen_name='home_screen', direction='right')
        self.app.lieu_choice = None
        self.app.plan_nettoyage_choice = None
        self.app.collaborateur_choice = None

    def clear_screen(self):
        clean_widget(self.plan_nettoyage_data["plan_nettoyage_selection_lieu_grid"])
        clean_widget(self.plan_nettoyage_data["plan_nettoyage_selection_plan_nettoyage"])
        clean_widget(self.plan_nettoyage_data["plan_nettoyage_selection_collaborateur_grid"])
