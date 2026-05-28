import pyxel as p

class App:
    def __init__(self):
        p.init(256, 256, title="Tower Defense")
        p.load("theme.pyxres")

        self.map = Map()
        # self.manche = Manche()
        self.joueur = Joueur(Manche())

        p.run(self.update, self.draw)

    def update(self):
        self.joueur.update()

    def draw(self):
        self.map.draw()
        self.joueur.draw_hud()

class Map:
    def __init__(self):
        self.tiles = [ [ '' for _ in range(16) ] for _ in range(16) ]
        self.chemin = ((0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(10,1),(10,2),(11,2),(12,2),(12,3),(12,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(9,9),(10,4),(11,4),(12,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),(3,12),(2,12),(1,12),(1,13),(1,14),(2,14),(3,14),(4,14),(5,14),(5,13),(5,12),(5,11),(5,10),(5,9),(6,9),(7,9),(8,9),(9,8),(9,7),(10,7),(11,7),(12,7),(12,8),(12,9),(12,10),(12,11),(12,12),(12,13),(12,14),(13,14),(14,14),(14,15),(15,15))

    def draw(self):
        p.rect(0, 0, 256, 256, 11)
        for element in self.chemin:
            p.rect(element[0]*16,element[1]*16,16,16,10)
            self.tiles[element[0]][element[1]] = "c"

class Manche:
    def __init__(self):
        self.manche = 1

class Tour:
    def __init__(self, type_tour, x, y, taille, distance, degat, vitesse, prix):
        self.type = type_tour
        self.x = x
        self.y = y
        self.taille = taille
        self.distance = distance

        self.niveau = 1
        self.degat = degat
        self.vitesse = vitesse
        self.prix = prix

class Joueur:
    def __init__(self, manche: Manche):
        self.argent = 1000
        self.manche = manche

    def draw_hud(self):
        p.text(233, 1, "Tour " + str(self.manche.manche), 0)
        p.text(252 - (4 * len(str(self.argent))), 7, str(self.argent) + "$" , 0)

    def update(self):
        #self.draw_hud()
        pass

App()