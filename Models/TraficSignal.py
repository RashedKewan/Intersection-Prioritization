import pygame
from .TraficSignalLightMode import TraficSignalLightMode as tslm
from .TraficSignalPositionMode import TraficSignalPositionMode as tspm
from .Directions import Directions


class TraficSignal:
    time = 5
    

    def __init__(self, WIN, x_position, y_position, image, position_mode, light_mode, direction):
        self.WIN = WIN
        self.x_position = x_position
        self.y_position = y_position
        self.image = image
        self.position_mode = position_mode
        self.light_mode = light_mode
        self.direction = direction

    def update_lights(self):
        HORIZONAL_POSITIONS_DIFFRENCE = -17
        VERTICAL_POSITIONS_DIFFRENCE = 17

        if self.position_mode is tspm.HORIZONAL:

            if self.direction is Directions.LEFT:
                diff_factor = int(Directions.LEFT.value) * HORIZONAL_POSITIONS_DIFFRENCE
            if self.direction is Directions.RIGHT:
                diff_factor = int(Directions.RIGHT.value) * HORIZONAL_POSITIONS_DIFFRENCE

            if self.light_mode is tslm.RED:
                self.turn_off_light(self.x_position+ diff_factor, self.y_position)  # YELLOW
                self.turn_off_light(self.x_position + 2*diff_factor, self.y_position)  # GREEN
                #self.WIN.blit(self.image, (531, 409))
                #self.WIN.blit(self.image, (514, 409))

            elif self.light_mode is tslm.YELLOW:
                self.turn_off_light(self.x_position , self.y_position)  # RED
                self.turn_off_light(self.x_position + 2*diff_factor, self.y_position)  # GREEN

            elif self.light_mode is tslm.GREEN:
                self.turn_off_light(self.x_position , self.y_position)  # RED
                self.turn_off_light(self.x_position + diff_factor, self.y_position)  # YELLOW

        elif self.position_mode is tspm.VERTICAL:

            if self.direction is Directions.UP:
                diff_factor = int(Directions.UP.value) * VERTICAL_POSITIONS_DIFFRENCE
            if self.direction is Directions.DOWN:
                diff_factor = int(Directions.DOWN.value) * VERTICAL_POSITIONS_DIFFRENCE

            if self.light_mode is tslm.RED:
                self.turn_off_light(self.x_position , self.y_position + diff_factor)  # YELLOW
                self.turn_off_light(self.x_position , self.y_position + 2*diff_factor)  # GREEN

            elif self.light_mode is tslm.YELLOW:
                self.turn_off_light(self.x_position , self.y_position)  # RED
                self.turn_off_light(self.x_position , self.y_position + 2*diff_factor)  # GREEN

            elif self.light_mode is tslm.GREEN:
                self.turn_off_light(self.x_position , self.y_position)  # RED
                self.turn_off_light(self.x_position , self.y_position + diff_factor)  # YELLOW

    def turn_off_light(self, x, y):
        self.WIN.blit(self.image, (x, y))

    def update_time(self, newTime):
        global time
        time = newTime

    def add_time(self, sec):
        global time
        time = time + sec

    def get_original_time(self):
        return 5
