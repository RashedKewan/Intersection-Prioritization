from sys import exit
import numpy as np
import pygame
import time
import os
from Models.Button import Button
from Models.Car import Car
from Models.Image import Image
from Models.Road import Road


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
paused = True
road_map = np.zeros([1000, 1000], dtype=int)

# FINALS
ASSETS_PACKAGE = 'Assets'

# COLORS
GRAY = ((128, 128, 128))

# frames per scond
FPS = 60

# ROAD
road = Road(100, 0, Image(1000, 1000, ASSETS_PACKAGE,
            'loop road.png').create_image())

# IMAGES
START = Image(80, 80, ASSETS_PACKAGE, 'start.png').create_image()
STOP = Image(80, 80, ASSETS_PACKAGE, 'stop.png').create_image()

# BUTTON
start_button = Button(1100, 0, START, WIN)
stop_button = Button(1100, 0, STOP, WIN)


############################################################
#####################  FUNCTIONS  ##########################
############################################################


def draw_window(cars):
    global paused
    global stop_pressed, start_pressed
    start_pressed, stop_pressed = False, False

    WIN.fill(GRAY)
    WIN.blit(road.image, (road.x_position, road.y_position))

    for car in cars:
        WIN.blit(car.image, (car.x_position, car.y_position))

    if paused:
        start_pressed = start_button.draw()
        if start_pressed:
            paused = False
    else:
        stop_pressed = stop_button.draw()
        if stop_pressed:
            paused = True

    pos = pygame.mouse.get_pos()
    # print(pos)
    pygame.display.update()

# counter for trafic signal
def countdown(car, t):
    car.can_move = False
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    car.can_move = True


def move_car(car):
    global paused
    global road_map

    #road_map[car.y_position-road.x_position][car.y_position-road.y_position] = 0

    if not paused and car.can_move:
        if car.y_position < 400 and car.x_position == 120:
            car.y_position = car.y_position+car.speed

        elif car.y_position >= 400 and car.y_position < 490 and car.x_position < 240:
            car.x_position = car.x_position+5
            car.y_position = car.y_position+5

        elif car.x_position < 920 and car.y_position == 490 and not car.intersection_detected:
            car.x_position = car.x_position + car.speed

        elif car.y_position < 570 and car.x_position < 1000 and car.x_position >= 920:
            car.x_position = car.x_position + 5
            car.y_position = car.y_position + 5
            car.intersection_detected = True

        elif car.y_position <= 800 and car.x_position >= 1000:
            car.y_position = car.y_position+car.speed

        elif car.y_position >= 800 and car.y_position <= 900 and car.x_position > 900 and car.x_position <= 1000:
            car.y_position = car.y_position+5
            car.x_position = car.x_position-5

        elif car.y_position > 900 and car.x_position > 700:
            car.x_position = car.x_position-car.speed

        elif car.y_position > 790 and car.x_position > 590:
            car.x_position = car.x_position - 5
            car.y_position = car.y_position - 5

        elif car.y_position > 90 and car.intersection_detected:
            car.y_position = car.y_position - car.speed

        elif car.x_position > 520 and car.y_position > 20 and car.y_position <= 100:
            car.x_position = car.x_position - 5
            car.y_position = car.y_position - 5
            car.intersection_detected = False

        elif car.y_position <= 35 and car.x_position < 520 and car.x_position > 220:
            car.x_position = car.x_position - car.speed
        else:
            car.y_position = car.y_position+5
            car.x_position = car.x_position-5
        ########### overriding cars problem
        # if road_map[car.y_position-road.x_position + 80][car.y_position-road.y_position] == 1  and car.x_position+80 < 920:
        #        car.speed = 5
        #road_map[car.y_position -road.x_position][car.y_position-road.y_position] = 1
        #print('( ', car.x_position, ' , ', car.y_position, ' )')


    ############ detect car with red signal light
    #if (445 == car.x_position) and (490 == car.y_position):
    #    countdown(car, 3)      
    return car

############################################################
########################  Main  ############################
############################################################

def main():
    clock = pygame.time.Clock()
    run = True

    # create cars
    yellow_car = Car(120, 100, Image(40, 40, ASSETS_PACKAGE,
                     'yellow car.png').create_image())
    green_car = Car(830, 490, Image(40, 40, ASSETS_PACKAGE,
                    'green car.png').create_image())
    red_car = Car(590, 670, Image(40, 40, ASSETS_PACKAGE,
                  'red car.png').create_image(), 15, True)
    cars = [yellow_car, green_car, red_car]


    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(cars)

        for car in cars:
            car = move_car(car)
    pygame.quit()


if __name__ == "__main__":
    main()
