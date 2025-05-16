import datetime as dt

# Class for tasks

class Task:

    def __init__(self, name, completed):
        self.name = name
        self.date = str(dt.datetime.now().date())
        self.completed = completed