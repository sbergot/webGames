import tornadio2.conn

class PlayersConnection(tornadio2.conn.SocketConnection):
    # Class level variable
    players = {}
    symbols = ["x", "o"]
    current = ["x"]

    def on_open(self, info):
        self.symbol = self.symbols.pop()
        self.players[self.symbol] = self
        self.emit('getsymbol', symbol=self.symbol)
        print "new player: ", self.symbol

    @tornadio2.event
    def play(self, box, fullGrid):
        if not self.current[0] == self.symbol:
            self.emit(
                'replay',
                status = "not your turn to play",
                grid = fullGrid)
            return
            
        if not grid.isfree(box):
            self.emit(
                'replay',
                status = "{} is already taken".format(box),
                grid = fullGrid)
            return

        grid.play(box, self.current[0])
        self.current[0] = "x" if self.current[0] == "o" else "o"
        status = grid.check_status()

        for p in self.players:
            self.players[p].emit('newturn', grid=grid.grid, status=status)

    @tornadio2.event
    def resetGrid(self, name):
        grid.reset()
        status=grid.check_status()
        for p in self.players:
            self.players[p].emit('newturn', grid=grid.grid, status=status)

    def on_close(self):
        self.players.pop(self.symbol)
        self.symbols.append(self.symbol)
