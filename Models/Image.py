import pygame
import os

class Image:
    def __init__(self,image_width, image_height, file_name, image_name):
        self.image_width = image_width
        self.image_height = image_height
        self.file_name = file_name
        self.image_name = image_name


    def create_image(self):
        image = pygame.image.load(os.path.join(self.file_name, self.image_name))
        output_image = pygame.transform.scale(
            image, (self.image_width, self.image_height))
        return output_image
