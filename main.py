from DBAccess import DBAccess
from TicketManager import TicketManager
from TonerAnalyzer import TonerAnalyzer
import json


class Manager:
    def __init__(self):
        self.db_access = DBAccess("report", "xVftpqiQyDssntxra", "pmsyglpi.byu.edu", 3306, "glpi")
        self.db_access.connect()
        self.ticket_manager = TicketManager("YW9uc3RvdHQ6Ym9ia2VlcHN0aW1lNzc=", "B2HA6LJIwSSLkVaGK4wQKdYFZbh5JBCh623wspMz", "https://pmsyglpi.byu.edu/apirest.php")
        self.toner_analyzer = TonerAnalyzer()

    def get_session_token(self):
        return self.ticket_manager.get_session_token()
    
    def get_low_toners(self):
        cartridge_levels = self.toner_analyzer.get_toner_levels()
        return self.toner_analyzer.find_low_toners(cartridge_levels)
    
    def create_tickets(self, session_token, low_toners):
        for toner in low_toners:
            ticket_name = toner.get_color() + " Toner Low at: " + toner.location

            #check if ticket already exists
            response = self.ticket_manager.search_tickets(session_token, toner.get_color(), toner.location)
            if response["totalcount"] > 0:
                print("Ticket already exists for: " + ticket_name)

            if toner.get_level() <= 10 and toner.get_level() > 5:
                print(toner.get_color() + " Toner at " + toner.location + " is at " + str(toner.level) + "%")
                print("Ticket will be created when toner level reaches 5% or lower.")
                
            elif toner.get_level() <= 5:
                ticket_description = toner.get_color() + " at " + toner.location + " is at " + str(toner.level) + "%"
                #response = self.ticket_manager.create_ticket(session_token, ticket_name, ticket_description)
                #if response status is in 200s, ticket was created successfully
                #if response.status_code >= 200 and response.status_code < 300:
                   # print("Ticket created for: " + ticket_name)
                    #print(json.dumps(response, indent=4))
                print("Ticket created for: " + ticket_name)
                print(ticket_description)


manager = Manager()
session_token = manager.get_session_token()
low_toners = manager.get_low_toners()
manager.create_tickets(session_token, low_toners)


        