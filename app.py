import pyxel as p

class App:
    def __init__(self):
        p.init(256, 256, title="Tower Defense")
        p.load("theme.pxres")

        self.map = Map()
        self.joueur = Joueur()

        p.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        self.map.draw()

class Map:
    def __init__(self):
        self.tiles = [ [ '' for _ in range(16) ] for _ in range(16) ]

    def draw(self):
        pass


class Joueur:
    def __init__(self):
        self.argent = 0