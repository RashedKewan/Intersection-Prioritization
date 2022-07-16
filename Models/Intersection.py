from Models.Image import Image


# effect
EFFECT_IMAGE = Image(16, 16, 'Assets', 'black-circle.png').create_image()


class Intersection:

    def __init__(self, WIN, traficSignalList):
        self.traficSignalList = traficSignalList
        self.WIN = WIN

    def build(self):
        for ts in self.traficSignalList :
            ts.update_lights()
