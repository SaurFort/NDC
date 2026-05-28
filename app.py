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

    def draw(self):
        p.rect(0, 0, 256, 256, 11)

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