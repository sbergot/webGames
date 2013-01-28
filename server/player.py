import tornadio2
import tornadio2.conn

import tic
grid = tic.Grid()
class PlayersConnection(tornadio2.conn.SocketConnection):
    # Class level variable
    players = {}
    symbols = ["x", "o"]
    current = ["x"]

    def on_open(self, info):
        self.symbol = self.symbols.pop()
        self.players[self.symbol] = self
        self.emit('getsymbol', symbol=self.symbol)

    @tornadio2.event
    def play(self, box, fullGrid):
        if not self.current[0] == self.symbol:
            self.emit(
                'play',
                status = "not your turn to play",
                grid = grid.grid)
            return
            
        if not grid.isfree(box):
            self.emit(
                'play',
                status = "{} is already taken".format(box),
                grid = grid.grid)
            return

        grid.play(box, self.current[0])
        self.current[0] = "x" if self.current[0] == "o" else "o"
        status = grid.check_status()

        for p in self.players:
            self.players[p].emit('play', grid=grid.grid, status=status)

    @tornadio2.event
    def resetGrid(self, name):
        grid.reset()
        status=grid.check_status()
        for p in self.players:
            self.players[p].emit('newturn', grid=grid.grid, status=status)

    def on_close(self):
        self.players.pop(self.symbol)
        self.symbols.append(self.symbol)
