from DBAccess import DBAccess
from Cartridge import Cartridge
from Credentials import Credentials

class TonerAnalyzer:
    def __init__(self):
        self.credentials = Credentials()
        self.db_access = DBAccess(self.credentials.username, self.credentials.password, self.credentials.host, self.credentials.host, self.credentials.database)
        self.db_access.connect()

    def get_toner_levels(self):
        cursor = self.db_access.conn.cursor()
        cursor.execute("SELECT * FROM glpi_printers_cartridgeinfos WHERE property = 'tonerblack' or property = 'tonercyan' or property = 'tonermagenta' or property = 'toneryellow'")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def find_low_toners(self, cartridges):
        low_toners = []
        for cartridge in cartridges:
            try:
                level = int(cartridge[3])
            except:
                print("Error: Toner level is not a number for cartridge: " + str(cartridge))
                continue
            if level <= 10:
                cartridge = Cartridge(cartridge[0], cartridge[1], cartridge[2], cartridge[3], self.get_toner_location(cartridge[1], cartridge[0]))
                low_toners.append(cartridge)
        return low_toners
    
    def get_toner_location(self, printer_id, cartridge_id):
        cursor = self.db_access.conn.cursor()
        cursor.execute("SELECT locations_id FROM glpi_printers WHERE id = " + str(printer_id))
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Error: Printer not found for cartridge: " + str(cartridge_id))
            return None
        elif len(rows) > 1:
            print("Error: Multiple printers found for cartridge: " + str(cartridge_id))
            return None
        else:
            location_id = rows[0][0]
            cursor.execute("SELECT completename FROM glpi_locations WHERE id = " + str(location_id))
            rows = cursor.fetchall()
            if len(rows) == 0:
                print("Error: Location not found for cartridge: " + str(cartridge_id))
                return None
            elif len(rows) > 1:
                print("Error: Multiple locations found for cartridge: " + str(cartridge_id))
                return None
            else:
                return rows[0][0]

#test
'''toner_analyzer = TonerAnalyzer()
cartridges = toner_analyzer.get_toner_levels()

low_toners = toner_analyzer.find_low_toners(cartridges)
for low_toner in low_toners:
    print(low_toner)'''


