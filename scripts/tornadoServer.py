from os import path as op
import tornado.web
from tornadio2 import TornadioRouter, SocketServer
import tic
import player

ROOT = op.normpath(op.dirname(__file__))
grid = tic.Grid()
GameRouter = TornadioRouter(player.PlayersConnection)
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
