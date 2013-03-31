from os import path as op
import tornado.web
from tornadio2 import TornadioRouter, SocketServer, SocketConnection
import tictactoe.connection
import tictactoe.model
import lobby
from session_broker import SESSION_BROKER

SESSION_BROKER.registerGame("tictactoe", tictactoe.model.TicTacToe)

ROOT = op.normpath(op.dirname(__file__))
BASE = op.join(ROOT, '..')

class MainConnection(SocketConnection):
    __endpoints__ = {
        '/tictactoe':tictactoe.connection.TicTacToeConnection,
        '/lobby':lobby.LobbyConnection,
        }

class FileServer(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")


HANDLERS = [
    (r'/app/(.*)',
     FileServer,
     {'path': op.join(BASE, "app"),
      'default_filename' : "index.html",}),
    (r'/test/(.+)',
     FileServer,
     {'path': op.join(BASE, "test")}),
    ]

GAME_ROUTER = TornadioRouter(MainConnection)

def config_server(socket_io_port, debug = False):
    return tornado.web.Application(
        GAME_ROUTER.apply_routes(HANDLERS),
        debug=debug,
        socket_io_port = socket_io_port
        )

def run():
    debug = True
    if debug:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    application = config_server(8001, debug)
    SocketServer(application)

if __name__ == "__main__":
    run()
