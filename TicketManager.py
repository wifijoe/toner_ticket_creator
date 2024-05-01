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
    
    #Params: session_token, toner_color, location
    #Returns: JSON response
    #Searches for tickets with the given toner color and location
    def search_tickets(self, session_token, toner_color, location):

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
            'criteria[1][value]': toner_color,
            'criteria[2][link]': 'AND',
            'criteria[2][field]': '83',
            'criteria[2][searchtype]': 'contains',
            'criteria[2][value]': location
        }



        response = requests.get(url, headers=headers, params=params) 
        return response.json()
    
    def create_ticket(self, session_token, ticket_name, ticket_description):
        headers = {
            "Session-Token": session_token,
            "App-Token": self.app_token
        }
        url = self.url + "/Ticket"

        data = {
            "input": {
                "name": ticket_name,
                "content": ticket_description,
                "status": 1
            }
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    

#test TicketManager
ticket_manager = TicketManager("YW9uc3RvdHQ6Ym9ia2VlcHN0aW1lNzc=", "B2HA6LJIwSSLkVaGK4wQKdYFZbh5JBCh623wspMz", "https://pmsyglpi.byu.edu/apirest.php")  
session_token = ticket_manager.get_session_token() 
print(ticket_manager.search_tickets(session_token, "jam", "BNSN"))

        