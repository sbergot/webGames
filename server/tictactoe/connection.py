import tornadio2
from gameconnection import GameConnection
import session
import model

class TicTacToeConnection(GameConnection):

    @tornadio2.event
    def play(self, box, symbol, fullGrid):
        result = self.game_session.model.play(box, symbol)
        if result["type"] == "error":
            self.emit_player('play', **result)
        else:
            self.broadcast('play', **result)

    @tornadio2.event
    def resetGrid(self, name):
        GAME.grid.reset()
        status=grid.check_status()
        self.broadcast('newturn', grid=grid.grid, status=status)
