from os import path as op
import tornado.web
from tornadio2 import TornadioRouter, SocketServer, SocketConnection
import player

ROOT = op.normpath(op.dirname(__file__))


class MainConnection(SocketConnection):
    __endpoints__ = {
        '/tictactoe':player.PlayersConnection,
        }

GameRouter = TornadioRouter(MainConnection)
handlers = [
    (r'/app/(.+)', tornado.web.StaticFileHandler, {'path': "app"}),
]
application = tornado.web.Application(
    GameRouter.apply_routes(handlers),
    debug=True,
    socket_io_port = 8001
    )
if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    SocketServer(application)
