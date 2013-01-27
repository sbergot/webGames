import tornadio2
import tornadio2.conn

class LobbyConnection(tornadio2.conn.SocketConnection):
    sessions = {
        "toto" : {"game" : "tictactoe", "id" : "toto"},
        "tata" : {"game" : "tictactoe", "id" : "tata"},
        }

    def on_open(self, data):
        self.emit('get_sessions', sessions=self.sessions.values())
