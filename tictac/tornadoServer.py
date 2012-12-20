import json
import tornado.ioloop
import tornado.web

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

class Play(tornado.web.RequestHandler):
    def post(self, box):
        self.set_header("Content-Type", "application/json")
        if not grid.isfree(box):
            self.write(json.dumps({"status" : "can't play {}".format(box), "grid" : grid.grid}))
            return

        grid.play(box, "x")
        status = grid.check_status()
        if status != "continue":
            self.write(json.dumps({"status" : status, "grid" : grid.grid}))
            return

        tic.play(grid)
        status = grid.check_status()
        self.write(json.dumps({
                "status" : status,
                "grid" : grid.grid
                }))

class Reset(tornado.web.RequestHandler):
    def post(self):
        grid.reset()

handlers = [
    (r'/css/(.+)', tornado.web.StaticFileHandler, {'path': "css"}),
    (r'/js/(.+)', tornado.web.StaticFileHandler, {'path': "js"}),
    (r'/', IndexHandler),
    (r'/tictactoe', TicTacToe),
    (r'/favicon.ico', Missing),
    (r'/play/(.*)', Play),
    (r'/reset', Reset)
]
application = tornado.web.Application(
    handlers,
    debug=True
    )

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
