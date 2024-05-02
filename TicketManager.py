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
            'criteria[2][value]': location,
            'criteria[3][link]': 'AND',
            'criteria[3][field]': '7',
            'criteria[3][searchtype]': 'contains',
            'criteria[3][value]': 'Needs Supplies',

        }



        response = requests.get(url, headers=headers, params=params) 
        return response.json()
    
    def create_ticket(self, session_token, ticket_name, ticket_description, location_id, printer_id):
        headers = {
            "Session-Token": session_token,
            "App-Token": self.app_token
        }
        url = self.url + "/Ticket"

        data = {
            "input": {
                "name": ticket_name,
                "content": ticket_description,
                "status": 1,
                "locations_id": location_id,
                "itilcategories_id": 1,
                "entities_id": 1,
                "items_id": printer_id,
                "requesttypes_id": 8
            }
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
    def link_ticket(self, session_token, ticket_id, item_id):
        headers = {
            "Session-Token": session_token,
            "App-Token": self.app_token
        }
        url = self.url + "/Item_Ticket"

        data = {
            "input": {
                "items_id": item_id,
                "tickets_id": ticket_id,
                "itemtype": "Printer"
            }
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
    def link_to_group(self, session_token, ticket_id, group_id):
        headers = {
            "Session-Token": session_token,
            "App-Token": self.app_token
        }
        url = self.url + "/Group_Ticket"

        data = {
            "input": {
                "groups_id": group_id,
                "tickets_id": ticket_id,
                "type": 2
            }
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    

#test TicketManager
ticket_manager = TicketManager("YW9uc3RvdHQ6Ym9ia2VlcHN0aW1lNzc=", "B2HA6LJIwSSLkVaGK4wQKdYFZbh5JBCh623wspMz", "https://pmsyglpi.byu.edu/apirest.php")  
session_token = ticket_manager.get_session_token()
print(ticket_manager.search_tickets(session_token, "Yellow", "CANC"))
#print(ticket_manager.create_ticket(session_token, "Test Ticket", "This is a test ticket", 1, 1))
#print(ticket_manager.link_ticket(session_token, 784, 9))

        