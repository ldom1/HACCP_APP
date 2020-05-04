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
            with open('refresh_token_file.txt', "w") as f:
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
            print(error_message)

    def exchange_refresh_token(self, refresh_token):
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_request = requests.post(refresh_url, data=refresh_payload)
        id_token = refresh_request.json()['id_token']
        local_id = refresh_request.json()['user_id']
        return id_token, local_id

    def sign_in(self):
        pass
