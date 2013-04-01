import tornadio2
import tornadio2.conn
from session_broker import SESSION_BROKER

class GameConnection(tornadio2.conn.SocketConnection):

    def broadcast(self, event, **kwargs):
        self.game_session.broadcast(event, kwargs)

    def register(self, player_id, session_id, player_name):
        self.player_id = player_id
        self.game_session = \
            SESSION_BROKER.get_session(session_id)
        self.get_player().connect(self)

    def get_player(self):
        return self.game_session.players[self.player_id]

    def unregister(self):
        try:
            self.game_session.disconnect(self, self.player_id)
        except AttributeError:
            pass

    @tornadio2.event
    def checkin(self, player_name, player_id, session_id):
        self.register(player_id, session_id, player_name)
        self.game_session.refresh_player(player_id)

    @tornadio2.event
    def quit(self, dummy):
        self.game_session.remove(self.player_id)
        self.close()

    def on_close(self):
        self.unregister()
        super(GameConnection, self).on_close()
