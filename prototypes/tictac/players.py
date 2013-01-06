import itertools

class Players:

    def __init__(self):
        self._players = set()
        self.reset()

    def reset(self):
        self.player_queue = itertools.cycle(self._players)

    def add(self, player):
        self._players.add(player)
        self.reset()

    def remove(self, player):
        self._players.remove(player)
        self.reset()

    def next(self):
        return self.player_queue.next()


if __name__ == "__main__":
    p = Players()
    p.add(1)
    p.add(2)
    p.add(3)
    p.add(8)
    for _ in range(10):
        print p.next()
    p.remove(3)
    for _ in range(10):
        print p.next()
