from typing import List
import TrafficSignal
import pygame
# vehicle typpes
CAR:str = 'car'
BUS:str = 'bus'
TRUCK:str = 'truck'
MOTORCYCLE:str = 'motorcycle'

# directions
RIGHT:str = 'right'
LEFT:str = 'left'
UP :str= 'up'
DOWN :str= 'down'




# LOOK IN DESIG FILE
points = {
     'A' : { 'x' : 175 , 'y' : 50 },
     'B' : { 'x' : 625 , 'y' : 50 },

     'C' : { 'x' : 300 , 'y' : 175 },
     'D' : { 'x' : 500 , 'y' : 175 },

     'E' : { 'x' : 300 , 'y' : 240 },
     'F' : { 'x' : 500 , 'y' : 240 },
     'G' : { 'x' : 625 , 'y' : 240 },
     'H' : { 'x' : 950 , 'y' : 240 },

     'I' : { 'x' : 175 , 'y' : 365 },
     'J' : { 'x' : 500 , 'y' : 365 },
     'K' : { 'x' : 625 , 'y' : 365 },
     'L' : { 'x' : 825 , 'y' : 365 },

     'M' : { 'x' : 625  , 'y' : 430 },
     'N' : { 'x' : 825  , 'y' : 430 },
     'O' : { 'x' : 950  , 'y' : 430 },
     'P' : { 'x' : 1275 , 'y' : 430 },

     'Q' : { 'x' : 500 , 'y' : 555 },
     'R' : { 'x' : 825 , 'y' : 555 },
     'S' : { 'x' : 950 , 'y' : 555 },
     'T' : { 'x' : 1150 , 'y' : 555 },

     'U' : { 'x' : 950 , 'y' : 620 },
     'V' : { 'x' : 1150 , 'y' : 620 },

     'W' : { 'x' : 825 , 'y' : 745 },
     'X' : { 'x' : 1275 , 'y' : 745 }
}

path = {
     1:[],
     2:[]
}

street_class = {
     RIGHT:0,
     LEFT:1,
     UP:2,
     DOWN:3
}
#lane_number = 

streets = {
     
     0:{         # RIGHT
          'CD':{
               'x':[300,500],
               'y':[175] # y max
          },
          'IJ':{
               'x':[300,500],
               'y':[365] # y max
          },
          'KL':{
               'x':[625,825],
               'y':[365] # y max
          },
          'ST':{
               'x':[950,1150],
               'y':[555] # y max
          },
          'QR':{
               'x':[500,825],
               'y':[555] # y max
          }
     ,
          'WX':{
               'x':[950,1150],
               'y':[745] # y max
          }
     },
     1:{         # LEFT
          'BA':{
               'x':[500,300],
               'y':[50] # y min
          },
          'FE':{
               'x':[500,300],
               'y':[240] # y min
          },
          'HG':{
               'x':[825,625],
               'y':[240] # y min
          },
          'NM':{
               'x':[825,625],
               'y':[430] # y min
          },
          'PO':{
               'x':[1150,950],
               'y':[430] # y min
          },
          'VU':{
               'x':[1150,950],
               'y':[620] # y min
          }
     },
     2:{         # UP
          'EC':{
               'x':[300], # x max
               'y':[240,175] 
          },
          'GB':{
               'x':[300], # x max
               'y':[240,175] 
          },
          'MK':{
               'x':[625], # x max
               'y':[430,365] 
          },
          'OH':{
               'x':[950], # x max
               'y':[430,365] 
          },
          'XP':{
               'x':[1275], # x max
               'y':[620,555] 
          },
          'US':{
               'x':[950], # x max
               'y':[620,555] 
          }
     },
     3:{         # DOWN
          'AI':{
               'x':[175], # x min
               'y':[175,240] 
          },
          'DF':{
               'x':[500], # x min
               'y':[175,240] 
          },
          'JQ':{
               'x':[625], # x min
               'y':[365,430] 
          },
          'LN':{
               'x':[825], # x min
               'y':[365,430] 
          },
          'RW':{
               'x':[825,885], # x min
               'y':[555,685] 
          },
          'TV':{
               'x':[1150,1215], # x min
               'y':[555,620] 
          }
     }
}



# define for each  'maslol'  it ' netev ' number
# random :select direction {R,L,U,D}
# select street vector .For EX: AI
# Random : select 'netev' number in choosen street vector



# Font Size
font_size:int = 30

# Colours
black = (0, 0, 0)
white = (255, 255, 255)

# Screensize
screen_width:int = 1100
screen_height:int = 900 #800
screen_size = (screen_width, screen_height)

# Loading signal images and font
#ronen change all image type to be with the image name , like this
red_signal_img= pygame.image.load('images/signals/red.png')
yellow_signal_img = pygame.image.load('images/signals/yellow.png')
green_signal = pygame.image.load('images/signals/green.png')
non_signal = pygame.image.load('images/signals/non.png')
background = pygame.image.load('images/street_900.png')
background_white = pygame.image.load('images/bg-white.png')


# Default values of signal times
default_red :int = 150
default_yellow:int = 3
default_green:int = 20
default_minimum:int = 10
default_maximum:int = 60

signals =[]
number_of_signals :int = 4
sim_time :int = 300       # change this to change time of simulation
time_elapsed :int = 0

current_green :int = 0   # Indicates which signal is green
next_green :int = (current_green + 1) % number_of_signals
current_yellow :int = 0   # Indicates whether yellow signal is on or off

# Average times for vehicles to pass the intersection
car_time :int = 2
motorcycle_time :int = 1
bus_time :float = 2.5
truck_time :float = 2.5

# Count of cars at a traffic signal
number_of_cars :int= 0
number_of_buses:int = 0
number_of_trucks :int= 0
number_of_motorcycle:int = 0
number_of_lanes:int = 2


# Red signal time at which cars will be detected at a signal
detection_time:int = 5

speeds:dict = {CAR: 2.25, BUS: 1.8, TRUCK: 1.8,
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
x:dict = {RIGHT: [0, 0, 0], DOWN: [755-z-245, 727-z-245, 697-z-245],
     LEFT: [1400, 1400, 1400], UP: [602+z, 627+z, 657+z]}
y:dict = {RIGHT: [348+z, 370+z, 398+z], DOWN: [0, 0, 0],
     LEFT: [498-z, 466-z, 436-z], UP: [800, 800, 800]}


vehicles:dict = {RIGHT: {0: [], 1: [], 2: [], 'crossed': 0}, DOWN: {0: [], 1: [], 2: [], 'crossed': 0},
            LEFT: {0: [], 1: [], 2: [], 'crossed': 0}, UP: {0: [], 1: [], 2: [], 'crossed': 0}}
#vehicleTypes = {0: CAR, 1: BUS, 2: TRUCK, 3: 'rickshaw', 4: MOTORCYCLE}
vehicle_types:dict = {
     0: CAR,
     1: BUS, 
     2: TRUCK, 
     3: MOTORCYCLE
     }
     
vehicles_weight = {
     MOTORCYCLE: 1,
     CAR: 4,
     TRUCK: 8,
     BUS: 20
     } 
direction_numbers = {0: RIGHT, 1: DOWN, 2: LEFT, 3: UP}

# Coordinates of signal image, timer, and vehicle count
signal_coordinates:list = [(350, 358), (350, 230), (440, 230), (440, 358)]
signal_timer_coordinates:list = [(355, 338), (355, 210), (445, 210), (445, 338)]
vehicle_count_coordinates:list = [(325, 338), (325, 210), (475, 210), (475, 338)]
vehicle_count_texts:list = ["0", "0", "0", "0"]

# Coordinates of stop lines
stop_lines:dict = {RIGHT: 590, DOWN: 330, LEFT: 800, UP: 535}
default_stop:dict = {RIGHT: 580, DOWN: 320, LEFT: 810, UP: 545}
stops:dict = {RIGHT: [580, 580, 580], DOWN: [320, 320, 320],
         LEFT: [810, 810, 810], UP: [545, 545, 545]}

mid:dict = {RIGHT: {'x': 705, 'y': 445}, DOWN: {'x': 695, 'y': 450},
       LEFT: {'x': 695, 'y': 425}, UP: {'x': 695, 'y': 450}}

rotate_factor = 70
directly = {RIGHT: {'x': 705-rotate_factor, 'y': 445+z}, DOWN: {'x': 695-z, 'y': 450-rotate_factor},
            LEFT: {'x': 695+rotate_factor - 20, 'y': 425-z}, UP: {'x': 695+z, 'y': 400+rotate_factor}}
   

rotation_angle = 3

# Gap between vehicles
gap = 15   # stopping gap
gap2 = 15   # moving gap
