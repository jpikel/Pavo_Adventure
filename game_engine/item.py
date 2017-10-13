class Item:
    active = False

    def __init__(self, id, title, action, location):
        self.id = id
        self.title= title
        self.action = action
        self.location = location

    def getName(self):
        return self.title

    def getLocation(self):
        return self.location

    def getId(self):
        return self.id

    def getAction(self):
        return self.action