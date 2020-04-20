# Temperature Fridge
import datetime
import json
import uuid

from kivy.app import App

import requests

from HaccpApp.haccpApp.src.pyScripts.utils import clean_widget


class ManageTemperatureFridgeScreen:

    def __init__(self):

        self.app = App.get_running_app()
        self.temperature_fridge_data = self.app.root.ids['operations_temperature_frigo_screen'].ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/test_user/operations/temperature_frigidaire.json"

    def modify_temperature_fridge_on_click(self, action):
        old_label_temp_fridge = self.temperature_fridge_data['label_temp_fridge'].text
        temp_old = float(old_label_temp_fridge.split()[0])
        if action == 'add':
            temp_new = temp_old + 0.1
        elif action == 'sub':
            temp_new = temp_old - 0.1
        else:
            temp_new = temp_old
        self.temperature_fridge_data['label_temp_fridge'].text = str(round(temp_new, 2)) + " °C"

    def get_data(self):

        temperature_fridge = self.temperature_fridge_data['label_temp_fridge'].text

        try:
            element_refrigerant_choice = self.app.element_refrigerant_choice
        except Exception as e:
            print(e)
            self.temperature_fridge_data['temp_fridge_warning'].text = "Veuillez sélectionner un élément réfrigérant"
            return
        try:
            collaborateur_choice = self.app.collaborateur_choice
        except Exception as e:
            print(e)
            self.temperature_fridge_data['temp_fridge_warning'].text = "Veuillez sélectionner un collaborateur"
            return

        self.temperature_fridge_data['temp_fridge_warning'].text = ""

        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"),
                'element_refrigerant': element_refrigerant_choice,
                'temperature': temperature_fridge,
                'collaborateur': collaborateur_choice,
                'id': str(uuid.uuid4())}

        response = requests.post(self.base_url, data=json.dumps(data))
        print(response.content.decode())

        self.app.change_screen(screen_name='home_screen', direction='right')

    def clear_temperature_fridge_screen(self):
        clean_widget(self.temperature_fridge_data["temp_frigo_selection_element_grid"])
        clean_widget(self.temperature_fridge_data["temp_frigo_selection_collaborateur_grid"])
        self.temperature_fridge_data['label_temp_fridge'].text = "3 °C"