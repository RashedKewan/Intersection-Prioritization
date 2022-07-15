import pygame


class Car:
    def __init__(self, x_position, y_position, image, speed=5, intersection_detected=False, can_move=True):
        self.x_position = x_position
        self.y_position = y_position
        self.image = image
        self.speed = speed
        self.can_move = can_move
        self.intersection_detected = intersection_detected
