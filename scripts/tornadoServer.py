import itertools
import json
import tornado.ioloop
import tornado.web
import tornadio2.conn
import tornadio2.router
import tornadio2.server

handlers = [
    (r'/(.+)', tornado.web.StaticFileHandler, {'path': "."}),
]
application = tornado.web.Application(
    handlers,
    debug=True,
    socket_io_port = 8001
    )

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
