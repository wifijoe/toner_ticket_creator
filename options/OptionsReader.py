class OptionsReader:
    def __init__(self):
        with open("options.cfg", "r", encoding="utf-8") as file:
            data = file.readlines()
        
        self.warn_level = int(self.get_attribute(data, "warn level"))
        self.create_level = int(self.get_attribute(data, "create ticket level"))
        



    def get_attribute(self, data, key):
        for line in data:
            if key in line:
                return line.split("=")[1].strip()