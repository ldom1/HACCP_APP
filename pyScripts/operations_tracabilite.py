#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
import uuid

from kivy.app import App

import requests

from pyScripts.utils import clean_widget


class ManageTracabiliteScreen:

    def __init__(self):

        self.app = App.get_running_app()
        self.screen_data = self.app.root.ids['operations_tracabilite_screen'].ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/{0}/operations/tracabilite.json?auth={1}".format(
            self.app.local_id,
            self.app.id_token)

    def get_data(self):

        try:
            source_img = self.screen_data['img_tracabilite_to_display'].source
            if source_img == "":
                self.screen_data['warning'].text = "Veuillez prendre en photo l'étiquette"
                return
        except Exception as e:
            print(e)
            self.screen_data['warning'].text = "Veuillez prendre en photo l'étiquette"
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
                'etiquette_img': source_img,
                'collaborateur': collaborateur_choice,
                'id': str(uuid.uuid4())}

        response = requests.post(self.base_url, data=json.dumps(data))
        print(response.content.decode())

        self.app.change_screen(screen_name='home_screen', direction='right')
        self.app.collaborateur_choice = None

    def clear_screen(self):
        clean_widget(self.screen_data["tracabilite_selection_collaborateur_grid"])
