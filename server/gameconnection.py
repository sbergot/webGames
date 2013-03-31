import tornadio2
import tornadio2.conn
from session_broker import SESSION_BROKER

class GameConnection(tornadio2.conn.SocketConnection):

    def broadcast(self, event, **kwargs):
        self.game_session.broadcast(event, kwargs)

    def register_session(self, player_id, session_id):
        self.game_session = \
            SESSION_BROKER.get_session(session_id)
        self.game_session.connect(self, player_id)
        self.player_id = player_id
        self.session_id = session_id

    def unregister(self):
        self.game_session.disconnect(self, self.player_id)

    def broadcast_player_list(self):
        self.broadcast('get-player-list',
                       players = self.game_session.get_slot_status())

    @tornadio2.event
    def checkin(self, player_name, player_id, session_id):
        self.register_session(player_id, session_id)
        self.emit_player(
            'get-symbol',
            symbol=self.game_session.get_symbol(player_id))
        self.emit_player(
            'get-status',
            status=self.game_session.get_status(player_id))
        self.broadcast_player_list()

    @tornadio2.event
    def quit(self, dummy):
        self.game_session.remove(self.player_id)
        self.broadcast_player_list()
        SESSION_BROKER.kill_if_dead(self.session_id)
        self.close()
    
    def emit_player(self, name, **data):
        self.game_session.emit(name, data, self.player_id)

    def on_close(self):
        self.unregister()
        super(GameConnection, self).on_close()
