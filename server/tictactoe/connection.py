import tornadio2
import player
import session
import model
import uuid

class TicTacToeConnection(player.GameConnection):

    @tornadio2.event
    def play(self, box, symbol, fullGrid):
        result = self.game_session.model.play(box, symbol)
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
        self.game_session = \
            session.SESSION_BROKER.get_session("tictactoe", session_id)
        self.game_session.addPlayer(self)
        self.emit('get-session-id', id=str(uuid.uuid4()))
        self.emit('getsymbol',
                  symbol=self.game_session.model.symbols.pop())
