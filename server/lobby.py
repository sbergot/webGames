import tornadio2
import tornadio2.conn
import session
import tictactoe.model

SESSIONS = {}
GAMES = {
    "tictactoe" : tictactoe.model.TicTacToe
    }

class LobbyConnection(tornadio2.conn.SocketConnection):
    sessions = {
        #"toto" : {"game" : "tictactoe", "id" : "toto"},
        #"tata" : {"game" : "tictactoe", "id" : "tata"},
        }

    def on_open(self, data):
        self.emit('get_sessions',
                  sessions=session.SESSION_BROKER.getSessions())

    def join(self):
        pass
