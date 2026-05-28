import pyxel as p
from random import *

class App:
    def __init__(self):
        p.init(256, 256, fps=30, title="Tower Defense")
        p.load("theme.pyxres")
        p.mouse(True)

        self.map = Map()
        #self.manche = Manche()
        #self.ennemi = Ennemi(1,1,self.map)
        self.manche = Manche(self.map)
        self.joueur = Joueur(self.manche, self.map)
        
        p.run(self.update, self.draw)

    def update(self):
        self.manche.update()
        self.joueur.update()

    def draw(self):
        self.map.draw()
        self.manche.draw()
        self.joueur.draw()

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
    def __init__(self,pv,degats, map: Map):
        self.pv = pv
        self.degats = degats
        self.x = 0
        self.y = 0
        self.map = map
        self.parcouru = [(0,0)]

    def draw(self):
        p.rect(self.y * 16,self.x * 16,16,16,3)

    def au_bout(self):
        return self.map.tiles[self.y][self.x] == "f"

    def deplacement(self):
        if self.map.tiles[self.y][self.x + 1] == "c" and (self.y,self.x+1) not in self.parcouru:
            self.parcouru.append((self.y,self.x+1))
            self.x += 1
        elif self.map.tiles[self.y][self.x - 1] == "c" and (self.y,self.x-1) not in self.parcouru:
            self.parcouru.append((self.y,self.x-1))
            self.x -= 1
        elif self.map.tiles[self.y + 1][self.x] == "c" and (self.y+1,self.x) not in self.parcouru:
            self.parcouru.append((self.y+1,self.x))
            self.y += 1
        elif self.map.tiles[self.y - 1][self.x] == "c" and (self.y-1,self.x) not in self.parcouru:
            self.parcouru.append((self.y-1,self.x))
            self.y -= 1

    def update(self):
        #self.draw()
        #p.rect(self.x * 16,self.y * 16,16,16,3)
        if self.x == 15 and self.y == 14:
            return True
        if self.map.tiles[self.y][self.x + 1] == "f":
            self.x += 1
        else:
            self.deplacement()


class Manche:
    def __init__(self, map: Map):
        self.manche = 0
        self.active = False
        self.map = map
        self.ennemis: list[Ennemi] = []
        self.joueur: Joueur

    def manche_suivante(self):
        self.manche += 1
        self.active = True
        self._spawn()

    def ennemi_vivant(self):
        if len(self.ennemis) == 0:
            self.active = False
            self.joueur.argent+=100

    def _spawn(self):
        for i in range (randint(self.manche,self.manche*10)):
            ennemi = Ennemi(1,1,self.map)
            self.ennemis.append(ennemi)

    def update(self):
        if self.active:
            self.joueur.action_tour(self.ennemis)
            self.ennemi_vivant()
            for ennemi in self.ennemis:
                if ennemi.pv <= 0:
                    self.ennemis.remove(ennemi)
                    self.joueur.argent += 10
                ennemi.update()
                if ennemi.au_bout():
                    self.ennemis.remove(ennemi)
                    self.joueur.perdre_vie(ennemi.degats)

    def draw(self):
        p.text(32, 32, str(len(self.ennemis)), 0)
        for ennemi in self.ennemis:
            ennemi.draw()

class Tour:
    def __init__(self, x, y, taille, distance, degat, vitesse, prix,  type_tour = "normal"):
        assert type_tour in ["normal"]
        self.type = type_tour
        self.x = x
        self.y = y
        self.taille = taille
        self.distance = distance
        self.valide = False

        self.niveau = 1
        self.degat = degat
        self.vitesse = vitesse
        self.prix = prix

    def preview_draw(self, map: Map):
        if self.type == "normal":
            p.rectb(self.x*16 - self.distance * 16, self.y*16 - self.distance * 16, self.distance * 32 + 16, self.distance * 32 + 16, 7)
            p.blt(self.x*16, self.y*16, 0, 0, 0, 16, 16)
            if self.valide:
                p.rectb(self.x*16, self.y*16, 16, 16, 0)
            else:
                p.rectb(self.x*16, self.y*16, 16, 16, 8)

    def peut_tirer(self, ennemi: Ennemi):
        tab = [ [ False for _ in range(15) ] for _ in range(16) ]
        tab[self.x][self.y] = True
        for j in range(1, self.distance + 1):
            for i in range(self.distance + 1):
                tab[self.x][self.y+i] = True
                tab[self.x][self.y-i] = True
                tab[self.x+j][self.y+i] = True
                tab[self.x+j][self.y-i] = True
                tab[self.x-j][self.y+i] = True
                tab[self.x-j][self.y-i] = True
        
        if tab[ennemi.y][ennemi.x]:
            return True
        return False

        
    def tir(self, ennemi: Ennemi):
        ennemi.pv -= self.degat

    def draw(self, map: Map):
        map.tiles[self.x][self.y] = "t-" + self.type
        if self.type == "normal":
            p.blt(self.x*16, self.y*16, 0, 0, 0, 16, 16)

class Joueur:
    def __init__(self, manche: Manche, carte: Map):
        self.argent = 200
        self.vie = 20
        self.manche = manche
        self.map = carte
        self.tours: list[Tour] = []
        self.placement = None

        self.manche.joueur = self

    def perdre_vie(self, degat):
        self.vie -= degat

    def action_tour(self, ennemis: list[Ennemi]):
        for tour in self.tours:
            for ennemi in ennemis:
                if tour.peut_tirer(ennemi):
                    tour.tir(ennemi)
                    break

    def update_sidebar(self):
        if p.btnp(p.MOUSE_BUTTON_LEFT):
            x = p.mouse_x
            y = p.mouse_y
            if self.argent >= 200:
                if x >= 240 and x <= 256 and y >= 32 and y <= 48:
                    self.argent -= 200
                    self.placement = Tour(7, 7, 1, 2, 1, 1, 200, "normal")

    def update_placement_tour(self):
        assert isinstance(self.placement, Tour)
        if p.btnp(p.KEY_BACKSPACE):
            self.argent += self.placement.prix
            self.placement = None
            return

        x = self.placement.x
        y = self.placement.y
        self.placement.valide = not self.map.tiles[x][y] in ["c", "s", "f"]

        if p.btnp(p.KEY_RIGHT) and x < 14:
            self.placement.x += 1
        if p.btnp(p.KEY_LEFT) and x > 0:
            self.placement.x -= 1
        if p.btnp(p.KEY_UP) and y  > 0:
            self.placement.y -= 1
        if p.btnp(p.KEY_DOWN) and y < 15:
            self.placement.y += 1 
        
        if p.btnp(p.KEY_RETURN) and self.placement.valide:
            self.placement.prix = 500
            self.tours.append(self.placement)
            self.placement = None

    def update(self):
        if not self.manche.active:
            self.update_sidebar()

            if self.placement:
                self.update_placement_tour()
            
            if p.btnp(p.KEY_E):
                self.manche.manche_suivante()
            
        if self.vie <= 0:
            pass

    def draw_hud(self):
        p.text(220 - (4 * len(str(self.manche.manche))), 1, "Tour " + str(self.manche.manche), 0)
        p.text(224 - (4 * len(str(self.vie))), 7, "Vie:" + str(self.vie), 0)
        p.text(236 - (4 * len(str(self.argent))), 13, str(self.argent) + "$" , 0)

        if not self.manche.active:
            p.text(96, 248, "E -> manche suivante", 0)

    def draw_tour(self):
        for tour in self.tours:
            tour.draw(self.map)

    def draw_sidebar(self):
        if self.argent >= 200:
            p.blt(240, 32, 0, 0 , 0, 16, 16)
            p.rectb(240, 32, 16, 16, 0)
        else:
            p.rect(240, 32, 16, 16, 0)
        p.text(241, 50, "200$", 7)

    def draw_placement_tour(self):
        assert isinstance(self.placement, Tour)
        self.placement.preview_draw(self.map)

    def draw(self):
        self.draw_hud()
        self.draw_tour()
        self.draw_sidebar()
        
        if self.placement:
            self.draw_placement_tour()

App()