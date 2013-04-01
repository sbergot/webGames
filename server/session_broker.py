import uuid
import event
from session import Session

class SessionBroker:
    """
    Stores the game session to show them in the lobby.
    Also stores the model constructors to create sessions.
    """

    def __init__(self):
        self.games = {}
        self.sessions = {}
        self.on_sessions_update = event.Event()

    def get_session(self, id):
        return self.sessions[id]

    def create_session(self, game):
        id = str(uuid.uuid4())
        session = Session(self.games[game])
        session.on_player_remove += lambda : self.kill_if_dead(id)
        self.sessions[id] = session
        self.on_sessions_update.fire()
        return id

    def registerGame(self, name, constructor):
        self.games[name] = constructor

    def get_sessions(self):
        res = {}
        for id in self.sessions:
            res[id] = self.sessions[id].get_description()
        return res

    def remove(self, id):
        del self.sessions[id]
        self.on_sessions_update.fire()

    def kill_if_dead(self, id):
        if not self.get_session(id).is_alive():
            self.remove(id)

SESSION_BROKER = SessionBroker()
