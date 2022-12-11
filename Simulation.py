# LAG
# NO. OF VEHICLES IN SIGNAL CLASS
# stops not used
# DISTRIBUTION
# BUS TOUCHING ON TURNS
# Distribution using python class

# *** IMAGE XY COOD IS TOP LEFT
import random
import math
import time
import threading
# from vehicle_detection import detection
import pygame
from gtts import gTTS
import os
from TrafficSignal import TrafficSignal
import GlobalData as GD
from Vehicle import VehicleClass

pygame.init()
simulation = pygame.sprite.Group()


# Initialization of signals with default values


def initialize():
    ts1 = TrafficSignal(
        red     = 0, 
        yellow  = GD.default_yellow, 
        green   = GD.default_green,
        minimum = GD.default_minimum, 
        maximum = GD.default_maximum
        )

    GD.signals.append(ts1)

    ts2 = TrafficSignal(
        red     = ts1.red + ts1.yellow + ts1.green, 
        yellow  = GD.default_yellow,
        green   = GD.default_green,
        minimum = GD.default_minimum,
        maximum = GD.default_maximum
        )

    GD.signals.append(ts2)

    ts3 = TrafficSignal(
        red     = GD.default_red, 
        yellow  = GD.default_yellow,
        green   = GD.default_green,
        minimum = GD.default_minimum,
        maximum = GD.default_maximum
        )

    GD.signals.append(ts3)

    ts4 = TrafficSignal(
        red     = GD.default_red, 
        yellow  = GD.default_yellow, 
        green   = GD.default_green, 
        minimum = GD.default_minimum,
        maximum = GD.default_maximum
        )

    GD.signals.append(ts4)
    repeat()

# Set time according to formula


def increase_vehicle_counter(vehicle : VehicleClass):
    if(vehicle.crossed == 0):
        vclass = vehicle.vehicle_class
        if(vclass == GD.CAR):
            GD.number_of_cars += 1
        elif(vclass == GD.BUS):
            GD.number_of_buses += 1
        elif(vclass == GD.TRUCK):
            GD.number_of_trucks += 1
        elif(vclass == GD.MOTORCYCLE):
            GD.number_of_motorcycle += 1


def read_text_with_voice(text:str, language:str):
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("detectingVehiclesSound.mp3")
    os.system("start detectingVehiclesSound.mp3")


def set_time():
    text = "detecting vehicles, " + \
        GD.direction_numbers[(GD.current_green + 1) % GD.number_of_signals]
    language = 'en'
    #readTextWithVoice(text,language)
    #os.system("say detecting vehicles, " + GD.directionNumbers[(GD.currentGreen+1) % GD.noOfSignals])
    GD.number_of_cars       :int = 0
    GD.number_of_buses      :int = 0
    GD.number_of_trucks     :int = 0
    GD.number_of_motorcycle :int = 0
    
    for i in range(1, 3):
        number_of_vehicles_in_next_green:int = len(GD.vehicles_[GD.direction_numbers[GD.next_green]][i])
        for j in range(number_of_vehicles_in_next_green):
            vehicle = GD.vehicles_[GD.direction_numbers[GD.next_green]][i][j]
            increase_vehicle_counter(vehicle)

    
    green_time = math.ceil(
        (
        (GD.number_of_cars*GD.vehicles_weight[GD.CAR]) + 
        (GD.number_of_motorcycle*GD.vehicles_weight[GD.MOTORCYCLE]) + 
        (GD.number_of_buses*GD.vehicles_weight[GD.BUS]) + 
        (GD.number_of_trucks*GD.vehicles_weight[GD.TRUCK])  
        )
        /(GD.number_of_lanes)
        )

    print('Green Time: ', green_time)
    if(green_time < GD.default_minimum):
        green_time = GD.default_minimum
    elif(green_time > GD.default_maximum):
        green_time = GD.default_maximum
  
    GD.signals[(GD.current_green + 1) % (GD.number_of_signals)].green = green_time


def repeat():
    # while the timer of current green signal is not zero
    while(GD.signals[GD.current_green].green > 0):
        # printStatus()
        update_values()

        # set time of next green signal
        if(GD.signals[(GD.current_green + 1) % (GD.number_of_signals)].red == GD.detection_time):
            thread = threading.Thread(
                name="detection", target=set_time, args=())
            thread.daemon = True
            thread.start()
            # setTime()
        time.sleep(1)
        

    GD.current_yellow = 1   # set yellow signal on
    GD.vehicle_count_texts[GD.current_green] = "0"

    # reset stop coordinates of lanes and vehicles
    for i in range(0, 3):
        GD.stops[GD.direction_numbers[GD.current_green]][i] = GD.default_stop[GD.direction_numbers[GD.current_green]]
        for vehicle in GD.vehicles_[GD.direction_numbers[GD.current_green]][i]:
            vehicle.stop = GD.default_stop[GD.direction_numbers[GD.current_green]]

    # while the timer of current yellow signal is not zero
    while(GD.signals[GD.current_green].yellow > 0):
        # printStatus()
        update_values()
        time.sleep(1)
    GD.current_yellow = 0   # set yellow signal off

    # reset all signal times of current signal to default times
    GD.signals[GD.current_green].green = GD.default_green
    GD.signals[GD.current_green].yellow = GD.default_yellow
    GD.signals[GD.current_green].red = GD.default_red
    


    # set next signal as green signal
    GD.current_green = GD.next_green
    # set next green signal
    GD.next_green = (GD.current_green + 1) % GD.number_of_signals
    
    

    GD.current_yellow = 1   # set yellow signal on
    while(GD.signals[GD.current_green].yellow > 0):
        update_values()
        time.sleep(1)
   
    GD.signals[GD.current_green].yellow = GD.default_yellow
    GD.signals[GD.current_green].red = GD.default_red
    GD.current_yellow = 0   # set yellow signal off
   

    # set the red time of next to next signal as (yellow time + green time) of next signal
    GD.signals[GD.next_green].red = GD.signals[GD.current_green].yellow + \
                                    GD.signals[GD.current_green].green

    repeat()

# Print the signal timers on cmd


def printStatus():
    for i in range(0, GD.number_of_signals):
        if(i == GD.current_green):
            if(GD.current_yellow == 0):
                print(" GREEN TS", i+1, "-> r:",
                      GD.signals[i].red, " y:", GD.signals[i].yellow, " g:", GD.signals[i].green)
            else:
                print("YELLOW TS", i+1, "-> r:",
                      GD.signals[i].red, " y:", GD.signals[i].yellow, " g:", GD.signals[i].green)
        else:
            print("   RED TS", i+1, "-> r:",
                  GD.signals[i].red, " y:", GD.signals[i].yellow, " g:", GD.signals[i].green)
    print()

# Update values of the signal timers after every second


def update_values():
    for i in range(0, GD.number_of_signals):
        if(i == GD.current_green):
            if(GD.current_yellow == 0):
                GD.signals[i].green -= 1
                GD.signals[i].total_green_time += 1
            else:
                GD.signals[i].yellow -= 1
        else:
            GD.signals[i].red -= 1


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
            for i in range(GD.number_of_signals):
                print('Lane', i+1, ':',
                      GD.vehicles[GD.direction_numbers[i]]['crossed'])
                total_vehicles += GD.vehicles[GD.direction_numbers[i]]['crossed']
            print('Total vehicles passed: ', total_vehicles)
            print('Total time passed: ', GD.time_elapsed)
            print('No. of vehicles passed per unit time: ',
                  (float(total_vehicles) / float(GD.time_elapsed)))
            os._exit(1)


