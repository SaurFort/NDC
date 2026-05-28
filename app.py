import pyxel as p

class App:
    def __init__(self):
        p.init(256, 256, fps=10, title="Tower Defense")
        p.load("theme.pyxres")
        p.mouse(True)

        self.map = Map()
        # self.manche = Manche()
        self.ennemi = Ennemi(1,1,1,self.map)
        self.manche = Manche()
        self.joueur = Joueur(self.manche, self.map)
        
        p.run(self.update, self.draw)

    def update(self):
        self.manche.update()
        self.joueur.update()
        self.ennemi.update()

    def draw(self):
        self.map.draw()
        self.joueur.draw_hud()
        self.ennemi.draw()

class Map:
    def __init__(self):
        self.tiles = [ [ '' for _ in range(16) ] for _ in range(15) ]
        self.chemin = ((0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(10,1),(10,2),(11,2),(12,2),(12,3),(12,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(9,9),(10,4),(11,4),(12,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,10),(3,11),(3,12),(2,12),(1,12),(1,13),(1,14),(2,14),(3,14),(4,14),(5,14),(5,13),(5,12),(5,11),(5,10),(5,9),(6,9),(7,9),(8,9),(9,8),(9,7),(10,7),(11,7),(12,7),(12,8),(12,9),(12,10),(12,11),(12,12),(12,13),(12,14),(13,14),(14,14),(14,15))

    def draw(self):
        # Fond
        p.rect(0, 0, 240, 256, 11)
        p.rect(240, 0, 16, 256, 1)
        # Chemin
        for element in self.chemin:
            p.rect(element[0]*16,element[1]*16,16,16,10)
            self.tiles[element[0]][element[1]] = "c"
        
        
        self.tiles[0][0] = "s"
        self.tiles[14][15] = "f"
        p.text(2, 5, "Spawn", 0)
        p.text(227, 246, "Fin", 0)

class Ennemi:
    def __init__(self,pv,vitesse,degats, map: Map):
        self.pv = pv
        self.vitesse = vitesse
        self.degats = degats
        self.x = 0
        self.y = 0
        self.map = map
        self.parcouru = [(0,0)]

        #p.run(self.update, self.draw)

    def draw(self):
        p.rect(self.y * 16,self.x * 16,16,16,3)
        p.text(16, 16, str(self.x) + " " + str(self.y), 0)

    def deplacement(self):
        if self.x < 14 and self.map.tiles[self.y][self.x + 1] == "c" and (self.y,self.x+1) not in self.parcouru:
            self.parcouru.append((self.y,self.x+1))
            self.x += 1
        elif self.map.tiles[self.y][self.x - 1] == "c" and (self.y,self.x-1) not in self.parcouru:
            self.parcouru.append((self.y,self.x-1))
            self.x -= 1
        elif self.y < 15 and self.map.tiles[self.y + 1][self.x] == "c" and (self.y+1,self.x) not in self.parcouru:
            self.parcouru.append((self.y+1,self.x))
            self.y += 1
        elif self.map.tiles[self.y - 1][self.x] == "c" and (self.y-1,self.x) not in self.parcouru:
            self.parcouru.append((self.y-1,self.x))
            self.y -= 1

    def update(self):
        #self.draw()
        #p.rect(self.x * 16,self.y * 16,16,16,3)
        if self.map.tiles[self.y][self.x + 1] == "f":
            self.x += 1
        else:
            self.deplacement()


class Manche:
    def __init__(self):
        self.manche = 0
        self.active = False
        self.ennemis = []

    def manche_suivante(self):
        self.manche += 1
        self.active = True
        self._spawn()

    def ennemi_vivant(self):
        if len(self.ennemis) == 0:
            self.active = False

    def _spawn(self):
        ennemi = Ennemi(1, 1, 1)

    def update(self):
        self.ennemi_vivant()

class Tour:
    def __init__(self, x, y, taille, distance, degat, vitesse, prix,  type_tour = "normal"):
        assert type_tour in ["normal"]
        self.type = type_tour
        self.x = x
        self.y = y
        self.taille = taille
        self.distance = distance

        self.niveau = 1
        self.degat = degat
        self.vitesse = vitesse
        self.prix = prix

    def draw(self, map: Map):
        map.tiles[self.y][self.x] = "t-" + self.type
        if self.type == "normal":
            p.blt(self.x*16, self.y*16, 0, 0, 0, 16, 16)

class Joueur:
    def __init__(self, manche: Manche, carte: Map):
        self.argent = 50
        self.vie = 20
        self.manche = manche
        self.map = carte
        self.tours: list[Tour] = []

    def update_sidebar(self):
        pass

    def update(self):
        self.update_sidebar()

    def draw_hud(self):
        p.text(220 - (4 * len(str(self.manche.manche))), 1, "Tour " + str(self.manche.manche), 0)
        p.text(224 - (4 * len(str(self.vie))), 7, "Vie:" + str(self.vie), 0)
        p.text(236 - (4 * len(str(self.argent))), 13, str(self.argent) + "$" , 0)

    def draw_tour(self):
        for tour in self.tours:
            tour.draw(self.map)

    def draw_sidebar(self):
        p.blt(240, 32, 0, 0 , 0, 16, 16)
        p.rectb(240, 32, 16, 16, 0)
        p.text(243, 50, "50$", 7)

    def draw(self):
        self.draw_hud()
        self.draw_tour()
        self.draw_sidebar()

App()