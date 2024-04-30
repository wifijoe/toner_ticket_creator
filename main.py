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
            ticket_name = toner.get_color() + " Toner Low at: " + "location" #fix this
