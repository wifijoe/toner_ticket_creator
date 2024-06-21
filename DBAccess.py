import mariadb

class DBAccess:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
    
    def connect(self):
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

    
    def get_location_id(self, complete_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM glpi_locations WHERE completename = ? AND entities_id = 1", (complete_name,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            print("Error: Location not found for: " + complete_name)
            return None
        elif len(rows) > 1:
            print(rows)
            print("Error: Multiple locations found for: " + complete_name)
            return None
        else:
            return rows[0][0]

