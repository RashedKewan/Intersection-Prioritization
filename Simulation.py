import random
import time
import threading
import pygame
from gtts import gTTS
import os
from TrafficSignal import TrafficSignal
import GlobalData as GD
from Vehicle import VehicleClass
from Intersection import Intersection

pygame.init()
simulation = pygame.sprite.Group()



def run_thread(thread_name:str , thread_target):
    thread = threading.Thread(name=thread_name, target=thread_target, args=())
    thread.daemon = True
    thread.start()


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
    GD.intersections[GD.FGKJ] = Intersection(intersection=GD.FGKJ, start_coordinate=365, current_green=3)
    GD.intersections[GD.NOSR] = Intersection(intersection=GD.NOSR, start_coordinate=615, current_green=3)
    create_intersction_signals(intersection = GD.FGKJ )
    create_intersction_signals(intersection = GD.NOSR )
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



# Generating vehicles in the simulation
def get_lane_length(direction : str , lane_number : int , c_x : str , c_y : str ) -> int:
    if(direction in [GD.RIGHT , GD.LEFT]):
        return abs(GD.streets[direction][lane_number][c_x][1] -GD.streets[direction][lane_number][c_x][0])
    return abs(GD.streets[direction][lane_number][c_y][1] -GD.streets[direction][lane_number][c_y][0])
     

def coordinate_vehicle_on_screen(direction : str , image_dimention : int  ):  
    c_x = 'x' # coordinate x
    c_y = 'y' # coordinate x
    lane_number =  random.randint(0, 5)
    # Initialize vehicle_x , vehicle_y
    vehicle_x = GD.streets[direction][lane_number][c_x][0]
    vehicle_y = GD.streets[direction][lane_number][c_y][0]
    lanes=[0,1,2,3,4,5]

    # Calculate lane length
    lane_length = get_lane_length(direction = direction ,lane_number = lane_number , c_x = c_x , c_y = c_y )
    
    # Calculate the remaining place for given lane with wehicle length and the gap
    vehicle_legel_len = GD.lanes_quantity[direction][lane_number] + image_dimention + GD.gap 
    print(f" \
                         {GD.lanes_quantity} \n\
        lanes_quantity    : {GD.lanes_quantity[direction][lane_number]} \n\
        vehicle_legel_len : {vehicle_legel_len} \n\
        lane_length       : {lane_length}")
    # In case the lane is full with vehicles
    while( vehicle_legel_len > lane_length):
        # remove the selected lane from lanes list 
        lanes.remove(lane_number)
        # In case all lanes for given direction is full
        # we need to handle this case carefully such that to have the ability
        # to choose another direction
        if(len(lanes) != 0):
            lane_number = random.choice(lanes)
        else :
            print('-----------------------------')
            print("| Cant select another lane. |")
            print('-----------------------------')
            break
        lane_length = get_lane_length(direction = direction ,lane_number = lane_number , c_x = c_x , c_y = c_y )
        vehicle_legel_len = GD.lanes_quantity[direction][lane_number] + image_dimention + GD.gap 
    # if the vehicle the first vehicle at the lane in [ left , right]
    if(GD.lanes_quantity[direction][lane_number] == 0):
        if(vehicle_x == GD.streets[direction][lane_number][c_x][0]):
            if(direction == GD.RIGHT ):
                vehicle_x+=image_dimention
            elif(direction == GD.LEFT ):
                vehicle_x-=image_dimention
        # if the vehicle the first vehicle at the lane in [ up , down ]
        elif(vehicle_y == GD.streets[direction][lane_number][c_y][0]):
            if(direction == GD.DOWN ):
                vehicle_y+=image_dimention
            elif(direction == GD.UP ):
                vehicle_y-=image_dimention
    else:
        # not the first 
        if(direction == GD.RIGHT ):
            vehicle_x+=vehicle_legel_len
        elif(direction == GD.LEFT ):
            vehicle_x-=vehicle_legel_len
        if(direction == GD.DOWN ):
            vehicle_y+=vehicle_legel_len
        elif(direction == GD.UP ):
            vehicle_y-=vehicle_legel_len

    GD.lanes_quantity[direction][lane_number] = vehicle_legel_len

    return lane_number,vehicle_x,vehicle_y



def choose_lane(direction_number:str,vehicle:str):
    path = f"images//{direction_number}//{vehicle}.png"
    image = pygame.image.load(path)
    image_dimention = image.get_rect().height
    if(direction_number in [GD.RIGHT , GD.LEFT]):
        image_dimention = image.get_rect().width
    return coordinate_vehicle_on_screen(direction_number,image_dimention)
   



def generate_vehicle():
   
    for vehicle_ , generation_number  in GD.vehicles_generating.items():
        for _ in range(generation_number):
            #vehicle_type = random.randint(0, 3)
            direction_number = random.randint(0,3)
            #lane_number,vehicle_x,vehicle_y = choose_lane(GD.direction_numbers[direction_number],GD.vehicle_types[vehicle_type]) 
            lane_number,vehicle_x,vehicle_y = choose_lane(GD.direction_numbers[direction_number],vehicle_)
            will_turn_left , will_turn_right = decide_if_will_turn(lane_number = lane_number)
    
            vehicle = VehicleClass(
                lane            = lane_number, 
                vehicle_class   = vehicle_, 
                direction       = GD.direction_numbers[direction_number], 
                will_turn_right = will_turn_right, 
                will_turn_left  = will_turn_left,
                x               = vehicle_x,
                y               = vehicle_y
                )
            GD.vehicles_[GD.direction_numbers[direction_number]][lane_number].insert(0,vehicle)
            vehicle.print()
            time.sleep(0.3)
       


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
            os._exit(1)


