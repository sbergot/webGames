import tornadio2
from gameconnection import GameConnection

class TicTacToeConnection(GameConnection):

    @tornadio2.event
    def play(self, box, symbol, fullGrid):
        self.game_session.model.play(box, symbol)

    @tornadio2.event
    def resetGrid(self, name):
        self.game_session.model.reset_grid()
