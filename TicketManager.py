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
    
    def print_search_options(self, session_token):
        headers = {
            "Session-Token": session_token,
            "App-Token": self.app_token
        }
        url = self.url + "/listSearchOptions/Ticket"

        response = requests.get(url, headers=headers)
        return response.json()
    
    #calls search endpoint to check if an open ticket for toner already exists
    def search_tickets(self, session_token, ticket_name):
        print(session_token)
        headers = {
            "Session-Token": session_token,
            "App-Token": self.app_token
        }
        url = self.url + "/search/Ticket"

        params = {
            'is_deleted': '0',
            'criteria[0][field]': '12',
            'criteria[0][searchtype]': 'equals',
            'criteria[0][value]': 'notold',
            'criteria[1][link]': 'AND',
            'criteria[1][field]': '1',
            'criteria[1][searchtype]': 'contains',
            'criteria[1][value]': ticket_name
        }

        response = requests.get(url, headers=headers, params=params)
        print("printed")
        return response.content

        