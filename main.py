"""
Main Module that gives code for analyzing and creating low toner tickets for the
GLPI system.
"""
import time
import os
from DBAccess import DBAccess
from TicketManager import TicketManager
from TonerAnalyzer import TonerAnalyzer
from Credentials import Credentials

os.chdir('/home/pharosbacon/toner_ticket_creator')

class Manager:
    """
    Manages the process of analyzing toner levels, excluding printers, 
    and creating tickets for low toner levels in the GLPI system.

    Attributes:
        credentials: Credentials for accessing the GLPI system.
        db_access: Access to the database for querying and storing data.
        ticket_manager: Manages ticket creation and interaction with the GLPI system.
        toner_analyzer: Analyzes toner levels for printers.
        blacklist: List of printer IDs to exclude from ticket creation.
    """
    def __init__(self):
        self.credentials = Credentials()
        self.db_access = DBAccess(self.credentials.username, self.credentials.password,
                                  self.credentials.host, self.credentials.port,
                                  self.credentials.database)
        self.db_access.connect()
        self.ticket_manager = TicketManager(self.credentials.auth, self.credentials.app_token,
                                            self.credentials.api_url)
        self.toner_analyzer = TonerAnalyzer()
        self.blacklist = []

    def get_session_token(self):
        """
        Retrieves a session token for authenticating requests to the GLPI system.

        Returns:
            str: Session token for the GLPI system.
        """
        return self.ticket_manager.get_session_token()

    def get_low_toners(self):
        """
        Retrieves the toner levels and identifies low toner levels.

        Returns:
            list: List of low toner objects.
        """
        cartridge_levels = self.toner_analyzer.get_toner_levels()
        return self.toner_analyzer.find_low_toners(cartridge_levels)

    def exclude_printers(self):
        """
        Excludes printers from ticket creation by reading printer IDs from the blacklist file.

        The blacklist file (`./options/blacklist.txt`) contains a list of printer IDs
        to exclude from ticket creation.
        """
        with open("options/blacklist.txt", "r", encoding="utf-8") as file:
            for line in file:
                self.blacklist.append(int(line))

    def create_tickets(self, session_token, low_toners):
        """
        Creates tickets for low toner levels in the GLPI system.

        For each low toner, it checks if a ticket already exists or if the printer is
        blacklisted. If a ticket doesn't exist, it creates a new ticket in the GLPI system.

        Args:
            session_token (str): The session token for authenticating the GLPI API requests.
            low_toners (list): List of low toner objects to process.
        """
        print("\n\nTHERE ARE CURRENTLY " + str(len(low_toners)) + " LOW TONERS:\n")
        for toner in low_toners:
            print(toner)
        print("\n")
        for toner in low_toners:
            if toner.printer_id in self.blacklist:
                print("Printer with id:" + str(toner.printer_id) + " is blacklisted. Skipping...\n")
                continue
            ticket_exists = False
            ticket_name = toner.get_color() + " Toner Low at: " + toner.location
            colors = []
            if toner.get_color() == "Black":
                colors.append("k toner")
                colors.append("toner k")
                colors.append("toner black")
                colors.append("black toner")
                colors.append("black")
            elif toner.get_color() == "Cyan":
                colors.append("n toner")
                colors.append("toner c")
                colors.append("toner cyan")
                colors.append("cyan toner")
                colors.append("cyan")
            elif toner.get_color() == "Magenta":
                colors.append("a toner")
                colors.append("toner m")
                colors.append("toner magenta")
                colors.append("magenta toner")
                colors.append("magenta")
            elif toner.get_color() == "Yellow":
                colors.append("w toner")
                colors.append("toner y")
                colors.append("toner yellow")
                colors.append("yellow toner")
                colors.append("yellow")

            for color in colors:
                if ticket_exists is False:
                    response = self.ticket_manager.search_tickets(session_token,
                                                                  color, toner.location)
                    response2 = self.ticket_manager.search_closed_tickets(session_token,
                                    color, toner.location, self.ticket_manager.get_time_string(5))
                    if response["totalcount"] > 0:
                        for ticket in response["data"]:
                            if int(ticket['13']) == int(toner.printer_id):
                                print("Ticket already exists for: " + ticket_name)
                                ticket_exists = True
                                break
                    if response2["totalcount"] > 0:
                        for ticket in response2["data"]:
                            if int(ticket['13']) == int(toner.printer_id):
                                print("Ticket already exists for: " + ticket_name)
                                ticket_exists = True
                                break

            if ticket_exists:
                continue

            if toner.get_level() <= 10 and toner.get_level() > 5:
                print(toner.get_color() + " Toner at " + \
                      toner.location + " is at " + str(toner.level) + "%")
                print("Ticket will be created when toner level reaches 5% or lower.\n")

            elif toner.get_level() <= 5:
                ticket_description = toner.get_color() + " at " + \
                    toner.location + " is at " + str(toner.level) + \
                        "% <p> </p> <p><em>This ticket was created automatically</em></p>"
                location_id = self.db_access.get_location_id(toner.location)
                response = self.ticket_manager.create_ticket(session_token, ticket_name,
                                                             ticket_description,location_id,
                                                             toner.printer_id)
                ticket_id = response["id"]

                self.ticket_manager.link_ticket(session_token, ticket_id, toner.printer_id)
                self.ticket_manager.link_to_group(session_token, ticket_id, 2)
                print("Ticket created for: " + ticket_name + "\n")
                #print(json.dumps(response, indent=4))
                print(ticket_description)

def run():
    """
    Runs the Manager process to analyze toner levels, exclude printers, and create tickets.

    This function initializes a Manager instance, retrieves the session token, finds low toners,
    excludes printers based on the blacklist, and creates tickets for low toner levels.
    """
    manager = Manager()
    session_token = manager.get_session_token()
    low_toners = manager.get_low_toners()
    manager.exclude_printers()
    manager.create_tickets(session_token, low_toners)

if __name__ == "__main__":
    print("------------------------------------------------------------")
    print("Starting at " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    run()
    finish_time = time.time()
    finish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(finish_time))
    print("Finished at: " + finish_time)
    print("------------------------------------------------------------")
