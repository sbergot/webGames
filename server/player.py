
class Player:

    def __init__(self, symbol):
        self.connections = set()
        self.symbol = symbol

    def connect(self, conn):
        self.connections.add(conn)

    def disconnect(self, conn):
        self.connections.remove(conn)

    def is_alive(self):
        return len(self.connections) > 0

    def emit(self, event, data):
        for conn in self.connections:
            conn.emit(event, data)
