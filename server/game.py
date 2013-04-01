from event import Event

class Game(object):

    def __init__(self):
        self.on_status_update = Event()
        self.on_invalid_operation = Event()
