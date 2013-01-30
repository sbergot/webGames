import tornadio2
import tornadio2.conn

class GameConnection(tornadio2.conn.SocketConnection):
    players = {}

    def on_open(self, info):
        self.symbol = info["symbol"]
        self.players[self.symbol] = self

    def on_close(self):
        pass

    def broadcast(self, event, **kwargs):
        for p in self.players:
            self.players[p].emit(event, **kwargs)
