#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
from kivy.app import App

from pyScripts.settings import ManageSettings


class Login:
    wak = "AIzaSyCEW8ny6lyMVIkSt5r2r-h6zRNJlmr00eM"  # web api key

    def sign_up(self, username, email, password):
        app = App.get_running_app()
        # Send email and password to firebase

        # Firebase will return a local id token and authToken (idToken) and a refreshToken
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.wak
        signup_payload = {"email": email, "password": password, "returnSecureToken": True}
        print(signup_payload)
        sign_up_request = requests.post(signup_url, data=signup_payload)
        print(sign_up_request.ok)
        print(sign_up_request.content.decode())
        sign_up_data = json.loads(sign_up_request.content.decode())

        if sign_up_request.ok:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']
            # Save refreshToken to a file
            with open(app.refresh_token_file, "w") as f:
                f.write(refresh_token)

            # Save localId and idToken to a variable in main app
            app.local_id = localId
            app.id_token = idToken

            # Create  a new key
            mydata = {"email": email, "user_name": username}
            url = "https://haccpapp-40c63.firebaseio.com/{0}.json?auth={1}".format(localId, idToken)
            requests.put(url, data=json.dumps(mydata))

            app.settings = ManageSettings()

            app.change_screen("home_screen", direction="left")

        else:

            error_data = json.loads(sign_up_request.content.decode())
            error_message = error_data["error"]['message']
            if error_message == "EMAIL_EXISTS":
                self.sign_in_existing_user(email, password)
                app.root.ids['login_screen'].ids['login_message'].text = error_message.replace("_", " ")
                app.change_screen("home_screen", direction="left")
            else:
                app.root.ids['login_screen'].ids['login_message'].text = error_message.replace("_", " ")

    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_request = requests.post(refresh_url, data=refresh_payload)
        id_token = refresh_request.json()['id_token']
        local_id = refresh_request.json()['user_id']
        return id_token, local_id

    def sign_in_existing_user(self, email, password):
        """Called if a user tried to sign up and their email already existed."""
        signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.wak
        signin_payload = {"email": email, "password": password, "returnSecureToken": True}
        signin_request = requests.post(signin_url, data=signin_payload)
        sign_up_data = json.loads(signin_request.content.decode())
        app = App.get_running_app()

        if signin_request.ok == True:
            refresh_token = sign_up_data['refreshToken']
            localId = sign_up_data['localId']
            idToken = sign_up_data['idToken']
            # Save refreshToken to a file
            with open(app.refresh_token_file, "w") as f:
                f.write(refresh_token)

            # Save localId to a variable in main app class
            # Save idToken to a variable in main app class
            app.local_id = localId
            app.id_token = idToken
            app.settings = ManageSettings()
            app.change_screen("home_screen", direction="left")
        elif signin_request.ok == False:
            error_data = json.loads(signin_request.content.decode())
            error_message = error_data["error"]['message']
            app.root.ids['login_screen'].ids['login_message'].text = "EMAIL EXISTS - " + error_message.replace("_", " ")

    def sign_in(self):
        pass
