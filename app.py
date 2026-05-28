import pyxel as p

class App:
    def __init__(self):
        p.init(256, 256, title="Tower Defense")
        p.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pass