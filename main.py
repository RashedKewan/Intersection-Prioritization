from sys import exit
import pygame
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
handle_running = True
intersection_detected = False

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


def draw_window(car):
    global handle_running
    global stop_pressed, start_pressed
    start_pressed, stop_pressed = False, False

    WIN.fill(GRAY)
    WIN.blit(road.image, (road.x_position, road.y_position))
    WIN.blit(car.image, (car.x_position, car.y_position))

    if handle_running:
        start_pressed = start_button.draw()
        if start_pressed:
            handle_running = False
    else:
        stop_pressed = stop_button.draw()
        if stop_pressed:
            handle_running = True

    pos = pygame.mouse.get_pos()
    print(pos)
    pygame.display.update()


def move_yellow_car(car):
    global intersection_detected
    global handle_running

    if handle_running == False:
        if car.y_position < 400 and car.x_position == 120:
            car.y_position = car.y_position+10

        elif car.y_position >= 400 and car.y_position < 490 and car.x_position < 240:
            car.x_position = car.x_position+5
            car.y_position = car.y_position+5

        elif car.x_position < 920 and car.y_position == 490 and not intersection_detected:
            car.x_position = car.x_position + 10

        elif car.y_position < 570 and car.x_position < 1000 and car.x_position >= 920:
            car.x_position = car.x_position + 5
            car.y_position = car.y_position + 5
            intersection_detected = True

        elif car.y_position <= 800 and car.x_position >= 1000:
            car.y_position = car.y_position+10

        elif car.y_position >= 800 and car.y_position <= 900 and car.x_position > 900 and car.x_position <= 1000:
            car.y_position = car.y_position+5
            car.x_position = car.x_position-5

        elif car.y_position > 900 and car.x_position > 700:
            car.x_position = car.x_position-10

        elif car.y_position > 790 and car.x_position > 590:
            car.x_position = car.x_position - 5
            car.y_position = car.y_position - 5

        elif car.y_position > 90 and intersection_detected:
            car.y_position = car.y_position - 10

        elif car.x_position > 520 and car.y_position > 20 and car.y_position <= 100:
            car.x_position = car.x_position - 5
            car.y_position = car.y_position - 5
            intersection_detected = False

        elif car.y_position <= 35 and car.x_position < 520 and car.x_position > 220:
            car.x_position = car.x_position - 10
        else:
            car.y_position = car.y_position+5
            car.x_position = car.x_position-5
    return car


def main():
    clock = pygame.time.Clock()
    run = True
    yellow_car = Car(120, 100, Image(40, 40, 'Assets',
                     'yellow car.png').create_image())

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(yellow_car)
        yellow_car = move_yellow_car(yellow_car)
    pygame.quit()


if __name__ == "__main__":
    main()
