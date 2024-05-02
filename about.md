This program reads from the GLPI database to create tickets for printers that have toners with level at or below 5%

# <span style="color:#0099ff">Class DBAccess:</span>

*This class will access the maria db for GLPI and return any printers that have toner that needs replaced.  Also returns toner level.*

## Functions:

```connect():``` connects to the GLPI database <br>
```get_location_id(complete_name):```  gets the id of a location given its name

<br>

# <span style="color:#0099ff">Class TicketManager</span>

*This class stores structure containing tickets that already exist to avoid duplication.  Also Creates new tickets using GLPI API.*

## Functions:
```get_session_token():``` calls the GLPI API init_session endpoint to get a session token to use for other API calls. This currently uses Aaron's authorization which needs to be changed. 

```print_search_options(session_token):```prints searchable fields for tickets in the GLPI API. ```search_options.json``` contains the search options, so this function only needs to be used if search options are changed.