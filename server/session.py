import player

class Session:

    def __init__(self, model):
        self.players = {}
        self.model = model(self)

    def addPlayer(self, id, instance):
        self.players[id] = instance
        self.players[id].symbol = self.model.pop_symbol()

    def connect(self, conn, player_id):
        if player_id not in self.players:
            self.addPlayer(player_id, player.Player())
        self.players[player_id].connect(conn)

    def emit(self, event, data, player_id):
        self.players[player_id].emit(event, data)

    def broadcast(self, event, data):
        for player in self.players.values():
            player.emit(event, data)

    def get_symbol(self, player_id):
        return self.players[player_id].symbol

    def get_status(self, player_id):
        symbol = self.get_symbol(player_id)
        return self.model.get_status(symbol)

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

    def getSessions(self):
        res = {}
        for name in self.sessions:
            for id in self.sessions[name]:
                res[id] = {"game" : name, "id" : id}
        return res

SESSION_BROKER = SessionBroker()
