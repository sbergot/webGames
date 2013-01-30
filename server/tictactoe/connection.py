import tornadio2
import player
import session
import model

class TicTacToeConnection(player.GameConnection):
    SESSIONS = {}

    @tornadio2.event
    def play(self, box, symbol, fullGrid):
        result = GAME.play(box, symbol)
        if result["type"] == "error":
            self.emit('play', **result)
        else:
            self.broadcast('play', **result)

    @tornadio2.event
    def resetGrid(self, name):
        GAME.grid.reset()
        status=grid.check_status()
        self.broadcast('newturn', grid=grid.grid, status=status)

    @tornadio2.event
    def register(self, player_name, player_id, session_id):
        if session_id in self.SESSIONS:
            self.session = self.SESSIONS[session_id]
        else:
            self.session = session.Session(model.TicTacToe())
            self.SESSIONS[session_id] = self.session
        self.session.players.append(self)
        self.emit('getsymbol', symbol=self.session.symbols.pop())
