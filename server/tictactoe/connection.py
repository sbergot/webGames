import tornadio2
import player
import session
import model

class TicTacToeConnection(player.GameConnection):

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
        self.session = session.SESSION_BROKER.get_session("tictactoe", session_id)
        self.session.addPlayer(self)
        self.emit('getsymbol', symbol=self.session.symbols.pop())
