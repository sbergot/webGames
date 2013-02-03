class Session:

    def __init__(self, model):
        self.players = []
        self.model = model(self)

    def addPlayer(self, player):
        self.players.append(player)

class SessionBroker:

    def __init__(self):
        self.games = {}
        self.sessions = {}

    def get_session(self, game, id):
        if id not in self.sessions[game]:
            self.spawnSession(game, id)
        return self.sessions[game][id]

    def spawnSession(self, game, id):
        self.sessions[game][id] = Session(self.games[game])

    def registerGame(self, name, constructor):
        self.games[name] = constructor
        self.sessions[name] = {}

SESSION_BROKER = SessionBroker()
