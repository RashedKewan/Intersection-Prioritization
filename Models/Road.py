import pygame


class Road:
    def __init__(self, WIN, x_position, y_position, image):
        self.WIN = WIN
        self.x_position = x_position
        self.y_position = y_position
        self.image = image

    def build(self):
        self.WIN.blit(self.image, (self.x_position, self.y_position))
