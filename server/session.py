import player
import uuid

class Session:

    def __init__(self, model):
        self.players = {}
        self.model = model(self)

    def add_player(self, id):
        self.players[id] = player.Player(self.model.pop_symbol())

    def connect(self, conn, player_id):
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

    def get_players(self):
        return [
            {"id" : id, "symbol" : player.symbol}
            for id, player in self.players.items()]

    def get_description(self):
        players = self.get_players()
        return {
            "name" : self.model.name,
            "players" : len(players),
            "slots" : self.model.slot_nbr}

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

    def getSessions(self):
        res = {}
        for id in self.sessions:
            res[id] = self.sessions[id].get_description()
        return res

SESSION_BROKER = SessionBroker()
