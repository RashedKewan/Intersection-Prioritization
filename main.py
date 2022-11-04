import threading
import pygame
import Simulation as sim
import sys
import GlobalData as GD

def run_thread(thread_name:str , thread_target):
    thread = threading.Thread(name=thread_name, target=thread_target, args=())
    thread.daemon = True
    thread.start()


screen = pygame.display.set_mode(GD.screen_size)
pygame.display.set_caption("SIMULATION")
font = pygame.font.Font(None, GD.font_size)

def turn_signal_on(signal_img, index:int):
    screen.blit(signal_img, GD.signal_coordinates[index])



def display_signal_timer_and_vehicle_count_for_each_signal(signal_number:int , signal_texts : list ):
        signal_texts[signal_number] = font.render(str(GD.signals[signal_number].signal_text), True, GD.white, GD.black)
        screen.blit(signal_texts[signal_number], GD.signal_timer_coordinates[signal_number])
        displayText = GD.vehicles[GD.direction_numbers[signal_number]]['crossed']
        GD.vehicle_count_texts[signal_number] = font.render(str(displayText), True, GD.black, GD.white)
        screen.blit(GD.vehicle_count_texts[signal_number], GD.vehicle_count_coordinates[signal_number])


def display_the_vehicles():
    for vehicle in sim.simulation:
        screen.blit(vehicle.current_image, [vehicle.x, vehicle.y])
        vehicle.move()

def display_time_elapsed():
    time_elapsed_text = font.render(("Time Elapsed: " + str(GD.time_elapsed)), True, GD.black, GD.white)
    screen.blit(time_elapsed_text, (1100, 50))


class Main:
    #########################################################################################################################
    ####################################################    Threads   #######################################################
    #########################################################################################################################
    run_thread(thread_name="simulationTime" ,thread_target=sim.simulation_time)
    run_thread("initialization" ,sim.initialize)
    run_thread("generateVehicles" ,sim.generate_vehicle)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    #########################################################################################################################
    #######################################      Display Background In Simulation     #######################################
    #########################################################################################################################
        screen.blit(GD.background, (0, 0))   



    #########################################################################################################################
    #######################################  display signal and set timer according   #######################################
    #######################################  to current status: green, yello, or red  #######################################
    #########################################################################################################################

        for i in range(0, GD.number_of_signals):
            if(i == GD.current_green):
                if(GD.current_yellow == 1):
                    GD.signals[i].signal_text = GD.signals[i].yellow
                    turn_signal_on(signal_img=GD.yellow_signal_img, index=i)

                    
                else:
                    GD.signals[i].signal_text = GD.signals[i].green
                    if(GD.signals[i].green <= 6 and GD.signals[i].green > 0 and GD.signals[i].green % 2 == 0):
                        turn_signal_on(signal_img = GD.non_signal, index=i)
                        
                    elif(GD.signals[i].green <= 6 and GD.signals[i].green > 0 and GD.signals[i].green % 2 == 1):
                        turn_signal_on(signal_img = GD.green_signal, index=i)
                       
                    else :
                        turn_signal_on(signal_img = GD.green_signal, index=i)
    
            else:
                if(GD.signals[i].red <= 10):
                    GD.signals[i].signal_text = GD.signals[i].red 
                else:
                    GD.signals[i].signal_text = ""
                turn_signal_on(signal_img = GD.red_signal_img, index=i)
               

        signal_texts = ["", "", "", ""]
        for i in range(0, GD.number_of_signals):
            display_signal_timer_and_vehicle_count_for_each_signal(signal_number = i , signal_texts = signal_texts)

        display_time_elapsed()

        display_the_vehicles()

        pygame.display.update()
