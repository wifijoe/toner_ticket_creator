import requests
class TicketManager:
    def __init__(self, auth_token, app_token, url):
        self.auth_token = auth_token
        self.app_token = app_token
        self.url = url

    #calls initSession endpoint to get a session token
    def get_session_token(self):
        url = self.url + "/initSession"
        headers = {
            "Authorization": "basic " + self.auth_token,
            "App-Token": self.app_token
        }

        response = requests.get(url, headers=headers)
        return response.json()["session_token"]
