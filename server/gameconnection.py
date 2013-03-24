import tornadio2
import tornadio2.conn
from session import SESSION_BROKER

class GameConnection(tornadio2.conn.SocketConnection):

    def broadcast(self, event, **kwargs):
        self.game_session.broadcast(event, kwargs)

    @tornadio2.event
    def checkin(self, player_name, player_id, session_id):
        self.game_session = \
            SESSION_BROKER.get_session(session_id)
        self.game_session.connect(self, player_id)
        self.player_id = player_id
        self.emit_player(
            'get-symbol',
            symbol=self.game_session.get_symbol(player_id))
        self.emit_player(
            'get-status',
            status=self.game_session.get_status(player_id))

    def emit_player(self, name, **data):
        self.game_session.emit(name, data, self.player_id)
