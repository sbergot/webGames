import tornadio2
import tornadio2.conn

class GameConnection(tornadio2.conn.SocketConnection):

    def on_close(self):
        pass

    def broadcast(self, event, **kwargs):
        for player in self.game_session.players:
            player.emit(event, **kwargs)
