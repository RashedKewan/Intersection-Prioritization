import random
import time
import threading
import pygame
import os
from TrafficSignal import TrafficSignal
import GlobalData as GD

from Intersection import Intersection
import FileController as fc

pygame.init()
simulation = pygame.sprite.Group()



def run_thread(thread_name:str , thread_target):
    thread = threading.Thread(name=thread_name, target=thread_target, args=())
    thread.daemon = True
    thread.start()

from Vehicle import VehicleClass
def create_intersction_signals( intersection: int = GD.FGKJ  ):
    signals = []
    current_green = GD.intersections[ intersection ].current_green
    ts1 = TrafficSignal(
        red     = 0, 
        yellow  = GD.default_yellow, 
        green   = GD.default_green,
        minimum = GD.default_minimum, 
        maximum = GD.default_maximum
        )
    ts2 = TrafficSignal(
        red     = ts1.red + ts1.yellow + ts1.green, 
        yellow  = GD.default_yellow,
        green   = GD.default_green,
        minimum = GD.default_minimum,
        maximum = GD.default_maximum
        )
    ts3 = TrafficSignal(
        red     = GD.default_red, 
        yellow  = GD.default_yellow,
        green   = GD.default_green,
        minimum = GD.default_minimum,
        maximum = GD.default_maximum
        )
    ts4 = TrafficSignal(
        red     = GD.default_red, 
        yellow  = GD.default_yellow, 
        green   = GD.default_green, 
        minimum = GD.default_minimum,
        maximum = GD.default_maximum
        )               
    # list the signals
    signals.append(ts1) 
    signals.append(ts2)
    signals.append(ts3)
    signals.append(ts4)

    # shift signals current_green times
    while(current_green > 0):
        signals.insert(0,signals.pop())
        current_green -= 1
  
    GD.intersections[ intersection ].signals = signals

def initialize():
    GD.intersections[GD.FGKJ] = Intersection(intersection=GD.FGKJ, start_coordinate=365, current_green=1)
    GD.intersections[GD.NOSR] = Intersection(intersection=GD.NOSR, start_coordinate=615, current_green=1)
    create_intersction_signals(intersection = GD.FGKJ )
    create_intersction_signals(intersection = GD.NOSR )
    
    if(GD.algorithm_active):
        run_thread(thread_name="NOSR" ,thread_target=GD.intersections[GD.NOSR].repeat_)
        run_thread(thread_name="FGKJ" ,thread_target=GD.intersections[GD.FGKJ].repeat_)
    else:
        run_thread(thread_name="NOSR" ,thread_target=GD.intersections[GD.NOSR].repeat)
        run_thread(thread_name="FGKJ" ,thread_target=GD.intersections[GD.FGKJ].repeat)

def decide_if_will_turn(lane_number : int):
    will_turn_right = 0
    will_turn_left = 0
    if(lane_number == 2):
        will_turn_right = check_if_will_turn()
    elif (lane_number == 1):
        will_turn_left = check_if_will_turn()
    return will_turn_left , will_turn_right


def choose_direction():
    temp = random.randint(0, 999)
    direction_number = 0
    a = [400, 800, 900, 1000]
    if(temp < a[0]):
        direction_number = 0
    elif(temp < a[1]):
        direction_number = 1
    elif(temp < a[2]):
        direction_number = 2
    elif(temp < a[3]):
        direction_number = 3
    return direction_number



def prepare_vehicle_environment( ):  
    c_x              = 'x' # coordinate x
    c_y              = 'y' # coordinate x
    direction_number = random.randint(0,3)
    lane_number      =  random.randint(0, 5)
    lanes            = [0,1,2,3,4,5]
    directions       = [0,1,2,3]
    direction = GD.direction_numbers[direction_number]
    while( GD.generating_coordinates[direction][lane_number]['0'][1] and GD.generating_coordinates[direction][lane_number]['1'][1]):
        # remove the selected lane from lanes list 
        lanes.remove(lane_number)
        # In case all lanes for given direction is full
        if(len(lanes) != 0):
            lane_number = random.choice(lanes)
        else :
            # to choose another direction
            directions.remove(direction_number)
            if(len(directions) != 0):
                lanes            = [0,1,2,3,4,5]
                direction_number = random.choice(directions)
                direction = GD.direction_numbers[direction_number]
            else:
                print('-----------------------------')
                print("| Cant generate vehicle.    |")
                print('-----------------------------')
                return 0,0,0
    
    
    if(direction == GD.RIGHT or direction==GD.LEFT ):
        if(GD.generating_coordinates[direction][lane_number]['0'][1]):#if first place is full
            vehicle_x=GD.generating_coordinates[direction][lane_number]['1'][0]
            GD.generating_coordinates[direction][lane_number]['1'][1]=True
        elif(GD.generating_coordinates[direction][lane_number]['0'][1] == False):
            vehicle_x=GD.generating_coordinates[direction][lane_number]['0'][0] 
            GD.generating_coordinates[direction][lane_number]['0'][1]=True
        vehicle_y=GD.streets[direction][lane_number][c_y][0]


    if(direction == GD.DOWN or direction==GD.UP ):
        if(GD.generating_coordinates[direction][lane_number]['0'][1]):#if first place is full
            vehicle_y=GD.generating_coordinates[direction][lane_number]['1'][0]

            GD.generating_coordinates[direction][lane_number]['1'][1]=True
        elif(GD.generating_coordinates[direction][lane_number]['0'][1] == False ):
            vehicle_y=GD.generating_coordinates[direction][lane_number]['0'][0] 
            GD.generating_coordinates[direction][lane_number]['0'][1]=True

        vehicle_x=GD.streets[direction][lane_number][c_x][0]
    GD.cars_number=GD.cars_number-1
    return direction,lane_number,vehicle_x,vehicle_y




def generate_vehicle():
   
    for vehicle_ , generation_number  in GD.vehicles_generating.items():
        for _ in range(generation_number):
            direction,lane_number,vehicle_x,vehicle_y = prepare_vehicle_environment()
            will_turn_left , will_turn_right = decide_if_will_turn(lane_number = lane_number)
            
            vehicle = VehicleClass(
                lane            = lane_number, 
                vehicle_class   = vehicle_, 
                direction       = direction, 
                will_turn_right = will_turn_right, 
                will_turn_left  = will_turn_left,
                x               = vehicle_x,
                y               = vehicle_y
                )
            GD.vehicles_[direction][lane_number].append(vehicle)
            time.sleep(0.5)
       


def check_if_will_turn():
    temp = random.randint(0, 3)
    if(temp < 2):
        return 1
    return 0



def simulation_time():
    while(True):
        GD.time_elapsed += 1
        time.sleep(1)
        if(GD.time_elapsed == GD.sim_time):
            total_vehicles = 0
            print('Lane-wise Vehicle Counts')
    #         for intersection in GD.intersections.keys():
    #             for i in range(4):
    #                 print('Lane', i+1, ':',GD.intersection_lanes[intersection][GD.direction_numbers[i]]['crossed'])
    # #GD.vehicles[GD.direction_numbers[i]]['crossed'])
    #                 total_vehicles += GD.vehicles[GD.direction_numbers[i]]['crossed']
                
            print('Total vehicles passed: ', total_vehicles)
            print('Total time passed: ', GD.time_elapsed)
            print('No. of vehicles passed per unit time: ',
                  (float(total_vehicles) / float(GD.time_elapsed)))
            # time.sleep(1)
            # os._exit(1)


