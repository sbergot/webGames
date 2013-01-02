import itertools
import json
import tornado.ioloop
import tornado.web
import tornadio2.conn
import tornadio2.router
import tornadio2.server
import players

import tic
import render
grid = tic.Grid()
tictactoeRenderer = render.GamePresenter("tic tac toe", "tictactoe", ["tictactoe"])

class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render("index.html")

class TicTacToe(tornado.web.RequestHandler):
    def get(self):
        return self.write(tictactoeRenderer.render({}))

class Missing(tornado.web.RequestHandler):
    def get(self):
        return self.write("")

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
        #import pdb; pdb.set_trace()
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

        grid.play(box, "x")
        status = grid.check_status()

        for p in self.players:
            players[p].emit('newturn', grid=fullGrid, status=status)

    @tornadio2.event
    def resetGrid(self, name):
        grid.reset()
        for p in self.players:
            print p
            players[p].emit('newturn', grid=fullGrid, status=status)

    def on_close(self):
        self.players.pop(self.symbol)
        self.symbols.append(self.symbol)

GameRouter = tornadio2.router.TornadioRouter(PlayersConnection)
handlers = [
    (r'/css/(.+)', tornado.web.StaticFileHandler, {'path': "css"}),
    (r'/js/(.+)', tornado.web.StaticFileHandler, {'path': "js"}),
    (r'/', IndexHandler),
    (r'/tictactoe', TicTacToe),
    (r'/favicon.ico', Missing),
]
application = tornado.web.Application(
    GameRouter.apply_routes(handlers),
    debug=True,
    socket_io_port = 8001
    )

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    application.listen(8888)
    tornadio2.server.SocketServer(application)
