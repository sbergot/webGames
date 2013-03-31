import uuid
from session import Session

class SessionBroker:
    """
    Stores the game session to show them in the lobby.
    Also stores the model constructors to create sessions.
    """

    def __init__(self):
        self.games = {}
        self.sessions = {}

    def get_session(self, id):
        return self.sessions[id]

    def create_session(self, game):
        id = str(uuid.uuid4())
        session = Session(self.games[game])
        self.sessions[id] = session
        return id

    def registerGame(self, name, constructor):
        self.games[name] = constructor

    def get_sessions(self):
        res = {}
        for id in self.sessions:
            res[id] = self.sessions[id].get_description()
        return res

SESSION_BROKER = SessionBroker()
