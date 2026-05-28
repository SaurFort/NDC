import pyxel as p

class App:
    def __init__(self):
        p.init(256, 256, title="Tower Defense")
        p.load("theme.pyxres")

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
        self.chemin = ((0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(10,1),(10,2),(11,2),(12,2),(12,3),(12,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(9,9),(10,4),(11,4),(12,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),(3,12),(2,12),(1,12),(1,13),(1,14),(2,14),(3,14),(4,14),(5,14),(5,13),(5,12),(5,11),(5,10),(5,9),(6,9),(7,9),(8,9),(9,8),(9,7),(10,7),(11,7),(12,7),(12,8),(12,9),(12,10),(12,11),(12,12),(12,13),(12,14),(13,14),(14,14),(14,15),(15,15))

    def draw(self):
        p.rect(0, 0, 256, 256, 11)
        for element in self.chemin:
            p.rect(element[0]*16,element[1]*16,16,16,10)

class Joueur:
    def __init__(self):
        self.argent = 0

App()