from DBAccess import DBAccess
from TicketManager import TicketManager
db_access = DBAccess("report", "xVftpqiQyDssntxra", "pmsyglpi.byu.edu", 3306, "glpi")
db_access.connect()

#print a table of the first 10 rows of the glpi_tickets table

cursor = db_access.conn.cursor()
'''cursor.execute("SELECT * FROM glpi_tickets LIMIT 10")
rows = cursor.fetchall()

print("id | entities_id | name | date")
print("-------------------------------")
for row in rows:
    print(row[0], "|", row[1], "|", row[2], "|", row[3])

cursor.close()'''

#ticket_manager = TicketManager("YW9uc3RvdHQ6Ym9ia2VlcHN0aW1lNzc=", "B2HA6LJIwSSLkVaGK4wQKdYFZbh5JBCh623wspMz", "https://pmsyglpi.byu.edu/apirest.php")
#print(ticket_manager.get_session_token())

