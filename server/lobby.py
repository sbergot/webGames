import tornadio2
import tornadio2.conn
from session_broker import SESSION_BROKER

class LobbyConnection(tornadio2.conn.SocketConnection):
    pool = set()

    def broadcast_sessions(self):
        for conn in self.pool:
            conn.emit_sessions()

    def emit_sessions(self):
        self.emit('get-sessions',
                  sessions=SESSION_BROKER.get_sessions())

    def on_open(self, data):
        self.pool.add(self)
        SESSION_BROKER.on_sessions_update += self.broadcast_sessions
        self.emit_sessions()

    @tornadio2.event
    def join_game(self, player_id, session_id, player_name):
        try:
            session = SESSION_BROKER.get_session(session_id)
        except KeyError:
            self.emit("error", {"message" : "session not found"})
            return
        if session.is_full():
            self.emit("error", {"message" : "session is full"})
            return
        session.add_player(player_id, player_name)
        game_name = session.get_description()["name"]
        self.emit("get-session-access",
                  {"id" : session_id,
                   "name" : game_name})

    @tornadio2.event
    def create_game(self, player_id, game_name, player_name):
        session_id = SESSION_BROKER.create_session(game_name)
        session = SESSION_BROKER.get_session(session_id)
        session.add_player(player_id, player_name)
        self.emit("get-session-access",
                  {"id" : session_id,
                   "name" : game_name})

    def on_close(self):
        self.pool.remove(self)
        SESSION_BROKER.on_sessions_update -= self.broadcast_sessions
