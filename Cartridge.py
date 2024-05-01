class Cartridge:
    def __init__(self, id, printer_id, type, level, location):
        self.id = id
        self.printer_id = printer_id
        self.type = type
        self.level = level
        self.location = location

    def __str__(self):
        return "id: " + str(self.id) + ", printer_id: " + str(self.printer_id) + ", type: " + self.type + ", level: " + str(self.level) + ", location: " + self.location
    
    def get_color(self):
        if self.type == "tonerblack":
            return "Black"
        elif self.type == "tonercyan":
            return "Cyan"
        elif self.type == "tonermagenta":
            return "Magenta"
        elif self.type == "toneryellow":
            return "Yellow"
        else:
            return "unknown"
        
    def get_level(self):
        return int(self.level)