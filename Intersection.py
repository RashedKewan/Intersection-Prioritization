
import math
import threading
import time
import pygame
import GlobalData as GD
from Vehicle import VehicleClass

class Intersection:
    def __init__(self, intersection : int , start_coordinate : int , current_green : int = 0):
        self.intersection = intersection       
        self.signals =[]
        self.number_of_signals :int = 4

        self.current_green :int = current_green   # Indicates which signal is green
        
        self.next_green :int = (self.current_green + 1) % self.number_of_signals
        
        self.current_yellow :int = 0   # Indicates whether yellow signal is on or off

        # Count of cars at a traffic signal
        self.number_of_cars :int= 0
        self.number_of_buses:int = 0
        self.number_of_trucks :int= 0
        self.number_of_motorcycle:int = 0
        x = start_coordinate
        self.traffic_sign_arrow_coordinates:list    = [( x+5  , x-55), (x+5  , x-185), (x+95  , x-185), (x+95   , x-55)]
        self.signal_coordinates:list                = [( x    , x-35), (x    , x-165), (x+90  , x-165), (x+90   , x-35)]
        self.signal_timer_coordinates:list          = [( x-35 , x-15), (x-35 , x-145), (x+145 , x-145), (x+145  , x-15)] 
        self.vehicle_count_coordinates:list         = [( x-35 , x-45), (x-35 , x-185), (x+145 , x-185), (x+145  , x-45)]
        
        self.vehicle_count_texts:list = ["0", "0", "0", "0"]


    def update_values(self):
        for i in range(0, self.number_of_signals):
            if(i == self.current_green):
                if(self.current_yellow == 0):
                    self.signals[i].green -= 1
                    self.signals[i].total_green_time += 1
                else:
                    self.signals[i].yellow -= 1
            else:
                self.signals[i].red -= 1



    def increase_vehicle_counter(self,vehicle : VehicleClass ):
        if(vehicle.crossed == 0):
            vclass = vehicle.vehicle_class
            if(vclass == GD.CAR):
                self.number_of_cars += 1
            elif(vclass == GD.BUS):
                self.number_of_buses += 1
            elif(vclass == GD.TRUCK):
                self.number_of_trucks += 1
            elif(vclass == GD.MOTORCYCLE):
                self.number_of_motorcycle += 1
    

    def set_time(self):
            text = "detecting vehicles, " + \
                GD.direction_numbers[(self.current_green + 1) % self.number_of_signals]
            language = 'en'
            #readTextWithVoice(text,language)
            #os.system("say detecting vehicles, " + GD.directionNumbers[(GD.currentGreen+1) % GD.noOfSignals])
            self.number_of_cars       :int = 0
            self.number_of_buses      :int = 0
            self.number_of_trucks     :int = 0
            self.number_of_motorcycle :int = 0
            
            next_green_direction = GD.direction_numbers[self.next_green]
            next_green_lane      = GD.intersection_lanes[self.intersection][next_green_direction][0]
            number_of_vehicles_in_next_green:int = len(GD.vehicles_[next_green_direction][next_green_lane])

            for j in range(number_of_vehicles_in_next_green):
                vehicle = GD.vehicles_[GD.direction_numbers[self.next_green]][next_green_lane][j]
                self.increase_vehicle_counter(vehicle)

            # changed to adjust configuration without algorithim
            green_time = GD.default_green

            print('Green Time: ', green_time)
            if(green_time < GD.default_minimum):
                green_time = GD.default_minimum
            elif(green_time > GD.default_maximum):
                green_time = GD.default_maximum
        
            self.signals[(self.current_green + 1) % (self.number_of_signals)].green = green_time


    def repeat(self):
        
            # while the timer of current green signal is not zero
            while(self.signals[self.current_green].green > 0):
                # printStatus()
                self.update_values()

                # set time of next green signal
                if(self.signals[(self.current_green + 1) % (self.number_of_signals)].red == GD.detection_time):
                    thread = threading.Thread(
                        name="detection", target=self.set_time, args=())
                    thread.daemon = True
                    thread.start()
                    # setTime()
                time.sleep(1)
                

            self.current_yellow = 1   # set yellow signal on
            self.vehicle_count_texts[self.current_green] = "0"

            # reset stop coordinates of lanes and vehicles
            for i in range(0, 3):
                GD.stops[GD.direction_numbers[self.current_green]][i] = GD.default_stop[GD.direction_numbers[self.current_green]]
                for vehicle in GD.vehicles_[GD.direction_numbers[self.current_green]][i]:
                    vehicle.stop = GD.default_stop[GD.direction_numbers[self.current_green]]

            # while the timer of current yellow signal is not zero
            while(self.signals[self.current_green].yellow > 0):
                # printStatus()
                self.update_values()
                time.sleep(1)
            self.current_yellow = 0   # set yellow signal off

            # reset all signal times of current signal to default times
            self.signals[self.current_green].green = GD.default_green
            self.signals[self.current_green].yellow = GD.default_yellow
            self.signals[self.current_green].red = GD.default_red
            


            # set next signal as green signal
            self.current_green = self.next_green
            # set next green signal
            self.next_green = (self.current_green + 1) % self.number_of_signals
            #################################
            #weight=self.calculate_weight(self.current_green)
            #print("calculating weight for next green: ")
            #print(weight)
            #############################
            
            

            self.current_yellow = 1   # set yellow signal on
            while(self.signals[self.current_green].yellow > 0):
                self.update_values()
                time.sleep(1)
        
            self.signals[self.current_green].yellow = GD.default_yellow
            self.signals[self.current_green].red = GD.default_red
            self.current_yellow = 0   # set yellow signal off
        

            # set the red time of next to next signal as (yellow time + green time) of next signal
            self.signals[self.next_green].red = self.signals[self.current_green].yellow + \
                                            self.signals[self.current_green].green

            self.repeat()
#####################################################################
#####################################################################
##########CHANGEEEEEEE###############################################
#####################################################################
#####################################################################

    def set_time_(self): 
        self.signals[self.next_green].green = GD.default_green

    def calculate_weight(self,lane_direction):
        second_direction=0
        weight=0
        first_lane=GD.intersection_weights_for_lanes[self.intersection][GD.direction_numbers[lane_direction]][0]
        first_direction=GD.direction_numbers[lane_direction]
        second_lane=GD.intersection_weights_for_lanes[self.intersection][GD.direction_numbers[lane_direction]][1]
        if(first_direction==GD.RIGHT): 
            second_direction=GD.DOWN
        if(first_direction==GD.DOWN): 
            second_direction=GD.RIGHT
        if(first_direction==GD.LEFT): 
            second_direction=GD.UP
        if(first_direction==GD.UP): 
            second_direction=GD.LEFT
       
        for vehicle in GD.vehicles_[first_direction][first_lane]:
            weight = weight + GD.vehicles_weight[vehicle.vehicle_class]
        for vehicle in GD.vehicles_[second_direction][second_lane]:
            weight = weight + GD.vehicles_weight[vehicle.vehicle_class]
        return weight



    #min_vehicles_weights_per_signal = 5
    def update_values_(self):
        for i in range(0, self.number_of_signals):
            if(i == self.current_green):
                if(self.current_yellow == 0):
                    if ( self.calculate_weight(lane_direction = i) < 5):# min_vehicles_weights_per_signal):
                        max_weight  = self.set_next_green()
                        if(max_weight == 0):
                            self.signals[i].green=10
                        else:
                            self.signals[i].green=0
                    else:
                        self.signals[i].green -= 1
                        if(self.signals[i].green==5):
                            self.set_next_green()
                            
                else:
                    self.signals[i].yellow -= 1
            else:
                self.signals[i].red -= 1


    def set_next_green(self):
        max_weight = 0
        next_green = 0
        for signal in range (self.number_of_signals):
            if( signal != self.current_green ):
                weight=self.calculate_weight(signal)
                
                if( weight > max_weight ):
                    max_weight = weight
                    next_green = signal
        if(max_weight == 0):
            self.next_green :int = (self.current_green + 1) % self.number_of_signals
        else:
            self.next_green =  next_green
        return max_weight
            
    def repeat_(self):
            # while the timer of current green signal is not zero
            while(self.signals[self.current_green].green > 0):
                self.update_values_()
                
                # set time of next green signal
                if(self.signals[(self.next_green) % (self.number_of_signals)].red == GD.detection_time):
                    thread = threading.Thread(
                        name="detection", target=self.set_time_, args=())
                    thread.daemon = True
                    thread.start()
                time.sleep(1)
                

            self.current_yellow = 1   # set yellow signal on
            self.vehicle_count_texts[self.current_green] = "0"

            # while the timer of current yellow signal is not zero
            while(self.signals[self.current_green].yellow > 0):
                self.update_values_()
                time.sleep(1)
            self.current_yellow = 0   # set yellow signal off

            # reset all signal times of current signal to default times
            self.signals[self.current_green].green = GD.default_green
            self.signals[self.current_green].yellow = GD.default_yellow
            self.signals[self.current_green].red = GD.default_red

            # set next signal as green signal
            self.current_green = self.next_green
            
            self.current_yellow = 1   # set yellow signal on
            while(self.signals[self.current_green].yellow > 0):
                self.update_values_()
                time.sleep(1)
                
        
            self.signals[self.current_green].yellow = GD.default_yellow
            self.signals[self.current_green].red = GD.default_red
            self.current_yellow = 0   # set yellow signal off
        

            # set the red time of next to next signal as (yellow time + green time) of next signal
            self.signals[self.next_green].red = self.signals[self.current_green].yellow + self.signals[self.current_green].green

            self.repeat_()


