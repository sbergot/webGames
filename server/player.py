import tornadio2
import tornadio2.conn

class GameConnection(tornadio2.conn.SocketConnection):
    players = {}

    def on_close(self):
        pass

    def broadcast(self, event, **kwargs):
        for player in self.session.players:
            player.emit(event, **kwargs)
