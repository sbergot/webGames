class Session:

    def __init__(self, model):
        self.model = model()
        self.players = []
        self.model.players = self.players
