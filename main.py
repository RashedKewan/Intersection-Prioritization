from sys import exit
import numpy as np
import pygame
import time
import os
import concurrent.futures
from Models.Button import Button
from Models.Car import Car
from Models.Directions import Directions
from Models.Image import Image
from Models.Intersection import Intersection
from Models.Road import Road
from Models.TraficSignal import TraficSignal as tf
from Models.TraficSignalLightMode import TraficSignalLightMode
from Models.TraficSignalPositionMode import TraficSignalPositionMode


############################################################
########################  SETUP  ###########################
############################################################


pygame.init()
WIDTH, HEIGHT = 1200, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WINDOW_NAME = "Signal Trafic Simulation"
pygame.display.set_caption(WINDOW_NAME)


############################################################
########################  VARIABLES  #######################
############################################################

# VARS
PAUSE_MODE = True
road_map = np.zeros([1000, 1000], dtype=int)

# FINALS
ASSETS_PACKAGE = 'Assets'

# COLORS
GRAY = ((128, 128, 128))

# frames per scond
FPS = 60

# ROAD
ROAD_IMAGE = Image(1000, 1000, ASSETS_PACKAGE, 'loop road.png').create_image()
road = Road(WIN, 100, 0, ROAD_IMAGE)



# IMAGES
START_IMAGE = Image(80, 80, ASSETS_PACKAGE, 'start.png').create_image()
STOP_IMAGE = Image(80, 80, ASSETS_PACKAGE, 'stop.png').create_image()

# BUTTON
start_button = Button(1100, 0, START_IMAGE, WIN)
stop_button = Button(1100, 0, STOP_IMAGE, WIN)

# effect
EFFECT_IMAGE = Image(16, 16, ASSETS_PACKAGE, 'black-circle.png').create_image()


# Trafic Signals
trafic_signals = []
trafic_signals.append(tf(WIN,497,409,EFFECT_IMAGE,TraficSignalPositionMode.HORIZONAL,TraficSignalLightMode.RED ,Directions.LEFT))
trafic_signals.append(tf(WIN,687,578,EFFECT_IMAGE,TraficSignalPositionMode.HORIZONAL,TraficSignalLightMode.RED ,Directions.RIGHT))
trafic_signals.append(tf(WIN,677,397,EFFECT_IMAGE,TraficSignalPositionMode.VERTICAL,TraficSignalLightMode.RED ,Directions.UP))
trafic_signals.append(tf(WIN,506,586,EFFECT_IMAGE,TraficSignalPositionMode.VERTICAL,TraficSignalLightMode.RED ,Directions.DOWN))

# Intersection
intersection = Intersection(WIN , trafic_signals)

############################################################
#####################  FUNCTIONS  ##########################
############################################################

def set_play_pause_button():
    global PAUSE_MODE

    if PAUSE_MODE:
        start_pressed = start_button.draw()
        if start_pressed:
            PAUSE_MODE = False
    else:
        stop_pressed = stop_button.draw()
        if stop_pressed:
            PAUSE_MODE = True


def draw_window(cars):
    WIN.fill(GRAY)
    road.build()
    intersection.build()

    for car in cars:
        car.draw()

    set_play_pause_button()
    
    print(pygame.mouse.get_pos())
    pygame.display.update()



############################################################
########################  Main  ############################
############################################################


def main():
    global PAUSE_MODE
    clock = pygame.time.Clock()
    run = True

    # create cars
    yellow_car_image = Image(40, 40, ASSETS_PACKAGE,'yellow car.png').create_image()
    yellow_car = Car(WIN, 120, 100, yellow_car_image)


    green_car_image = Image(40, 40, ASSETS_PACKAGE,'green car.png').create_image()
    green_car = Car(WIN, 830, 490, green_car_image)
    
    red_car_image = Image(40, 40, ASSETS_PACKAGE,'red car.png').create_image()
    red_car = Car(WIN, 590, 670, red_car_image , 15, True)
    cars = [yellow_car, green_car, red_car]
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(cars)
   
        for car in cars:
            car = car.move_LR(PAUSE_MODE)

        """

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(car.move_LR ,[PAUSE_MODE]) for car  in cars]
            for f in concurrent.futures.as_completed(results):
                cars = f.result()
        """
    pygame.quit()


if __name__ == "__main__":
    main()
