from typing import List
import TrafficSignal
import pygame
# vehicle typpes
CAR = 'car'
BUS = 'bus'
TRUCK = 'truck'
MOTORCYCLE = 'motorcycle'

# directions
RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'


# Font Size
fontSize = 30

# Colours
black = (0, 0, 0)
white = (255, 255, 255)

# Screensize
screenWidth = 1400
screenHeight = 800
screenSize = (screenWidth, screenHeight)

# Loading signal images and font
#ronen change all image type to be with the image name , like this
red_signal_img = pygame.image.load('images/signals/red.png')
yellow_signal_img = pygame.image.load('images/signals/yellow.png')
greenSignal = pygame.image.load('images/signals/green.png')
nonSignal = pygame.image.load('images/signals/non.png')
background = pygame.image.load('images/mod_int.png')


# Default values of signal times
default_red :int = 150
default_yellow:int = 3
default_green:int = 20
default_minimum:int = 10
default_maximum:int = 60

signals =[]
#signals =[]
no_of_signals :int= 4
sim_time :int= 300       # change this to change time of simulation
time_elapsed :int= 0

current_green :int= 0   # Indicates which signal is green
next_green :int= (current_green + 1) % no_of_signals
current_yellow :int= 0   # Indicates whether yellow signal is on or off

# Average times for vehicles to pass the intersection
car_time :int= 2
MotorcycleTime :int= 1
busTime :float= 2.5
truckTime :float= 2.5

# Count of cars at a traffic signal
noOfCars :int= 0
noOfBuses = 0
noOfTrucks = 0
noOfMotorcycle = 0
noOfLanes = 2


# Red signal time at which cars will be detected at a signal
detectionTime = 5

speeds = {CAR: 2.25, BUS: 1.8, TRUCK: 1.8,
          MOTORCYCLE: 2.5}  # average speeds of vehicles


# Coordinates of start
# x = direction : lane <- { 0 , 1 , 2 }
"""
x = {RIGHT: [0, 0, 0], DOWN: [755, 727, 697],
     LEFT: [1400, 1400, 1400], UP: [602, 627, 657]}
y = {RIGHT: [348, 370, 398], DOWN: [0, 0, 0],
     LEFT: [498, 466, 436], UP: [800, 800, 800]}
"""
z = 66
x = {RIGHT: [0, 0, 0], DOWN: [755-z, 727-z, 697-z],
     LEFT: [1400, 1400, 1400], UP: [602+z, 627+z, 657+z]}
y = {RIGHT: [348+z, 370+z, 398+z], DOWN: [0, 0, 0],
     LEFT: [498-z, 466-z, 436-z], UP: [800, 800, 800]}


vehicles = {RIGHT: {0: [], 1: [], 2: [], 'crossed': 0}, DOWN: {0: [], 1: [], 2: [], 'crossed': 0},
            LEFT: {0: [], 1: [], 2: [], 'crossed': 0}, UP: {0: [], 1: [], 2: [], 'crossed': 0}}
#vehicleTypes = {0: CAR, 1: BUS, 2: TRUCK, 3: 'rickshaw', 4: MOTORCYCLE}
vehicleTypes = {
     0: CAR,
     1: BUS, 
     2: TRUCK, 
     3: MOTORCYCLE
     }
     
vehiclesWeight = {
     MOTORCYCLE: 1,
     CAR: 4,
     TRUCK: 8,
     BUS: 20
     } 
directionNumbers = {0: RIGHT, 1: DOWN, 2: LEFT, 3: UP}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(546, 550), (546, 250), (794, 250), (794, 550)]
signalTimerCoods = [(560, 530), (560, 230), (810, 230), (810, 530)]
vehicleCountCoods = [(495, 530), (495, 230), (880, 230), (880, 530)]
vehicleCountTexts = ["0", "0", "0", "0"]

# Coordinates of stop lines
stopLines = {RIGHT: 590, DOWN: 330, LEFT: 800, UP: 535}
defaultStop = {RIGHT: 580, DOWN: 320, LEFT: 810, UP: 545}
stops = {RIGHT: [580, 580, 580], DOWN: [320, 320, 320],
         LEFT: [810, 810, 810], UP: [545, 545, 545]}

mid = {RIGHT: {'x': 705, 'y': 445}, DOWN: {'x': 695, 'y': 450},
       LEFT: {'x': 695, 'y': 425}, UP: {'x': 695, 'y': 450}}

rotate_factor = 70
directly = {RIGHT: {'x': 705-rotate_factor, 'y': 445+z}, DOWN: {'x': 695-z, 'y': 450-rotate_factor},
            LEFT: {'x': 695+rotate_factor - 20, 'y': 425-z}, UP: {'x': 695+z, 'y': 400+rotate_factor}}
   

rotationAngle = 3

# Gap between vehicles
gap = 15   # stopping gap
gap2 = 15   # moving gap
