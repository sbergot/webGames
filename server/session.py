import event
from player import Player

class Session:
    """
    Holds a game model and a pool of players.  A session offers
    communication between players & common game operations.
    """

    def __init__(self, model):
        self.players = {}
        self.symbol_map = {}
        self.on_player_remove = event.Event()
        self.model = model()
        self.model.on_status_update += self.broadcast_status_update
        self.model.on_invalid_operation += self.emit_error

    def add_player(self, id, name):
        if id in self.players:
            return
        player = Player(name, self.model.pop_symbol())
        self.players[id] = player
        self.symbol_map[player.symbol] = player
        self.broadcast_player_list()

    def broadcast_player_list(self):
        self.broadcast('get-player-list',
                       {"players" : self.get_slot_status()})

    def broadcast_status_update(self):
        for player in self.players.values():
            player.emit('update-status',
                        self.model.get_status(player.symbol))

    def emit_error(self, symbol, message):
        self.symbol_map[symbol].emit('error',
                                     {"message" : message})

    def remove(self, id):
        del self.symbol_map[self.players[id].symbol]
        del self.players[id]
        self.broadcast_player_list()
        self.on_player_remove.fire()

    def refresh_player(self, id):
        player = self.players[id]
        symbol = player.symbol
        player.emit(
            'get-symbol',
            {"symbol" : symbol})
        player.emit(
            'update-status',
            self.model.get_status(symbol))
        player.emit('get-player-list',
                    {"players" : self.get_slot_status()})

    def is_alive(self):
      return bool(self.players)  

    def is_full(self):
      return len(self.players) == self.model.slot_nbr

    def disconnect(self, conn, player_id):
        player = self.players[player_id]
        player.disconnect(conn)
        if not player.is_alive():
            self.remove(player_id)

    def broadcast(self, event, data):
        for player in self.players.values():
            player.emit(event, data)

    def get_players(self):
        return [player.get_description()
                for player in self.players.values()]

    def get_slot_status(self):
        players = self.get_players()
        unoccupied = max(self.model.slot_nbr - len(players), 0)
        for _ in range(unoccupied):
            players.append(Player.empty())
        return players

    def get_description(self):
        return {"name" : self.model.name,
                "players" : len(self.get_players()),
                "slots" : self.model.slot_nbr}

