import tornadio2
import tornadio2.conn
import uuid
from session import SESSION_BROKER

class GameConnection(tornadio2.conn.SocketConnection):

    def broadcast(self, event, **kwargs):
        self.game_session.broadcast(event, kwargs)

    @tornadio2.event
    def register(self, player_name, player_id, session_id):
        self.game_session = \
            SESSION_BROKER.get_session("tictactoe", session_id)
        self.game_session.connect(self, player_id)
        self.emit('get-session-id', id=str(uuid.uuid4()))
        self.emit('get-symbol',
                  symbol=self.game_session.get_symbol(player_id))
