import game

class MyModel(game.Game):
    name = "my model"
    slot_nbr = 3

    def __init__(self):
        super(MyModel, self).__init__()
        self.symbols = [
            "fake symbol 1",
            "fake symbol 2",
            "fake symbol 3",
            ]

    def pop_symbol(self):
        return self.symbols.pop()

    def get_status(self, symbol):
        return "status for {}".format(symbol)
