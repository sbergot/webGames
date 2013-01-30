import tornadio2
import player

import model
GAME = model.TicTacToe()

class TicTacToeConnection(player.GameConnection):

    def on_open(self, info):
        symbol = GAME.symbols.pop()
        super(TicTacToeConnection, self).on_open({"symbol" : symbol})
        self.emit('getsymbol', symbol=symbol)

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
