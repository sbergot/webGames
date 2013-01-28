from os import path as op
import tornado.web
from tornadio2 import TornadioRouter, SocketServer, SocketConnection
import player
import lobby

ROOT = op.normpath(op.dirname(__file__))
BASE = op.join(ROOT, '..')

class MainConnection(SocketConnection):
    __endpoints__ = {
        '/tictactoe':player.PlayersConnection,
        '/lobby':lobby.LobbyConnection,
        }

GameRouter = TornadioRouter(MainConnection)
handlers = [
    (r'/app/(.*)',
     tornado.web.StaticFileHandler,
     {'path': op.join(BASE, "app"),
      'default_filename' : "index.html",}),
    (r'/test/(.+)',
     tornado.web.StaticFileHandler,
     {'path': op.join(BASE, "test")}),
]
application = tornado.web.Application(
    GameRouter.apply_routes(handlers),
    debug=True,
    socket_io_port = 8001
    )
def run():
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    SocketServer(application)

if __name__ == "__main__":
    run()
