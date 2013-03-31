
class Player:

    def __init__(self, name, symbol):
        self.connections = set()
        self.symbol = symbol
        self.name = name

    def connect(self, conn):
        self.connections.add(conn)

    def disconnect(self, conn):
        self.connections.remove(conn)

    def is_alive(self):
        return len(self.connections) > 0

    def emit(self, event, data):
        for conn in self.connections:
            conn.emit(event, data)

    def get_description(self):
        return {"symbol" : self.symbol,
                "name" : self.name,
                "occupied" : True}

    @classmethod
    def empty(cls):
        return {"occupied" : False,
                "name" : None,
                "symbol" : None}
