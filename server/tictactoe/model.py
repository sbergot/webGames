import random

def get_rows():
    rows = []
    for x in range(3):
        v = []
        h = []
        for y in range(3):
            v.append(box(x + 1, y + 1))
            h.append(box(y + 1, x + 1))
        rows.append(v)
        rows.append(h)
    rows.append(["11", "22", "33"])
    rows.append(["13", "22", "31"])
    return rows


def box(x, y):
    return u"{}{}".format(x, y)

def get_random_box():
    return box(random.randint(1, 3), random.randint(1, 3))

def play(grid):
    box = get_random_box()
    while not grid.isfree(box):
        box = get_random_box()
    grid.play(box, "o")

class Grid:

    def __init__(self):
        self.reset()

    def reset(self):
        self.grid =  [
            [{"coord" : "11", "value" : ""},
	     {"coord" : "12", "value" : ""},
	     {"coord" : "13", "value" : ""}],
	    [{"coord" : "21", "value" : ""},
	     {"coord" : "22", "value" : ""},
	     {"coord" : "23", "value" : ""}],
	    [{"coord" : "31", "value" : ""},
	     {"coord" : "32", "value" : ""},
	     {"coord" : "33", "value" : ""}]
            ]

    def isfree(self, box):
        return self.box(box)["value"] == ""

    def check_status(self):
        for row in get_rows():
            symbols = set(self.box(box)["value"] for box in row)
            if len(symbols) == 1 and u"" not in symbols:
                return  "player {} wins".format(symbols.pop())
        if "" in [box["value"] for row in self.grid for box in row]:
            return "continue"
        return "end"

    def box(self, cell):
	x = int(cell[0]) - 1;
	y = int(cell[1]) - 1;
        return self.grid[x][y]
        
    def play(self, box, symbol):
        if not self.isfree(box):
            raise Exception("{} is not free!".format(box))
        self.box(box)["value"] = symbol

class TicTacToe:

    def __init__(self):
        self.symbols = ["x", "o"]
        self.current = self.symbols[0]
        self.grid = Grid()

    def switch_player(self):
        self.current = "x" if self.current == "o" else "o"

    def play(self, box, symbol):
        if not self.current == symbol:
            return {
                "status" : "not your turn to play",
                "grid" : self.grid.grid,
                "type" : "error",
                }
            
        if not self.grid.isfree(box):
            return {
                "status" : "{} is already taken".format(box),
                "grid" : self.grid.grid,
                "type" : "error",
                }

        self.grid.play(box, symbol)
        self.switch_player()
        return {
            "status" : self.grid.check_status(),
            "grid" : self.grid.grid,
            "type" : "continue",
            }

if __name__ == "__main__":
    print get_rows()
