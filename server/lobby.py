import tornadio2
import tornadio2.conn
from session import SESSION_BROKER

class LobbyConnection(tornadio2.conn.SocketConnection):

    def on_open(self, data):
        self.emit('get_sessions',
                  sessions=SESSION_BROKER.getSessions())

    @tornadio2.event
    def join_game(self, player_id, session_id):
        session = SESSION_BROKER.get_session(session_id)
        session.add_player(player_id)

    @tornadio2.event
    def create_game(self, player_id, game_name):
        id = SESSION_BROKER.create_session(game_name)
        session = SESSION_BROKER.get_session(id)
        session.add_player(player_id)
        self.emit("get-session-id", {"id" : id})
