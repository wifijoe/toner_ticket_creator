This program reads from the GLPI database to create tickets for printers that have toners with level at or below 5%

```Class DBAccess:```
    This class will access the maria db for GLPI and return any printers that have toner that needs replaced.  Also returns toner level

```Class TicketManager```
    This class stores structure containing tickets that already exist to avoid duplication.  Also Creates new tickets using GLPI API.