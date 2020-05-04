#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
import uuid

from kivy.app import App

import requests

from pyScripts.utils import clean_widget


class ManageReceptionProduitScreen:

    def __init__(self):

        self.app = App.get_running_app()
        self.screen_data = self.app.root.ids['operations_reception_produit_screen'].ids
        self.base_url = "https://haccpapp-40c63.firebaseio.com/{0}/operations/reception_produit.json?auth={1}".format(
            self.app.local_id,
            self.app.id_token)

    def modify_temperature_on_click(self, action):
        old_label_temp_fridge = self.screen_data['label_temp_reception_produit'].text
        temp_old = float(old_label_temp_fridge.split()[0])
        if action == 'add':
            temp_new = temp_old + 0.1
        elif action == 'sub':
            temp_new = temp_old - 0.1
        else:
            temp_new = temp_old
        self.screen_data['label_temp_reception_produit'].text = str(round(temp_new, 2)) + " °C"

    def get_data(self):

        temperature_produit = self.screen_data['label_temp_reception_produit'].text

        try:
            fournisseur_choice = self.app.fournisseur_choice
            if not fournisseur_choice:
                self.screen_data['warning'].text = "Veuillez sélectionner un fournisseur"
                return
        except Exception as e:
            print(e)
            self.screen_data['warning'].text = "Veuillez sélectionner un fournisseur"
            return
        try:
            categorie_choice = self.app.categorie_choice
            if not categorie_choice:
                self.screen_data['warning'].text = "Veuillez sélectionner une catégorie"
                return
        except Exception as e:
            print(e)
            self.screen_data['warning'].text = "Veuillez sélectionner une catégorie"
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

        data = {'date': datetime.datetime.today().strftime("%d/%m/%Y %H:%M"), 'fournisseur': fournisseur_choice,
                'categorie': categorie_choice, 'collaborateur': collaborateur_choice,
                'temperature_produit': temperature_produit,
                'id': str(uuid.uuid4())}

        response = requests.post(self.base_url, data=json.dumps(data))
        print(response.content.decode())

        self.app.change_screen(screen_name='home_screen', direction='right')
        self.app.lieu_choice = None
        self.app.plan_nettoyage_choice = None
        self.app.collaborateur_choice = None

    def clear_screen(self):
        clean_widget(self.screen_data["reception_produit_selection_fournisseur_grid"])
        clean_widget(self.screen_data["reception_produit_selection_categorie_grid"])
        clean_widget(self.screen_data["reception_produit_selection_collaborateur_grid"])
        self.screen_data['label_temp_reception_produit'].text = "3 °C"
