
"""
logging class, takes the print() output and saves it to a file also
"""
import sys
from datetime import date

class Logger(object):
    """
    Redirects the standard output to a log file for better logging.

    Methods:
    - `write`: Writes messages to both the standard output and a log file.
    - `flush`: Handles the flush command for compatibility.
    """
    def __init__(self):
        """
        Initializes the Logger object.
        """
        self.terminal = sys.stdout

    def write(self, message):
        """
        Writes messages to both the standard output and a log file.

        Parameters:
        - message (str): The message to be written.
        """
        self.terminal.write(message)
        try:
            with open(f"logs/logfile_{date.today()}.log", "a+", encoding="utf-8") as file:
                file.write(message)
        except FileNotFoundError:
            with open(f"logs/logfile_{date.today()}.log", "w", encoding="utf-8") as file:
                file.write(message)

    def flush(self):
        """
        Handles the flush command for compatibility.
        """
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
