import os
import shutil
import threading
import pygame
import Simulation as sim
import sys
import GlobalData as GD
import FileController as fc
import PDFReport as pdf
from reportlab.pdfgen import canvas


def run_thread(thread_name:str , thread_target,args=()):
    thread = threading.Thread(name=thread_name, target=thread_target, args=args)
    thread.daemon = True
    thread.start()
    return thread





screen = pygame.display.set_mode(GD.screen_size)
pygame.display.set_caption("SIMULATION")
font = pygame.font.Font(None, GD.font_size)

def turn_signal_on(intersection :int, signal_img, index:int):
    screen.blit(signal_img, GD.intersections[intersection].signal_coordinates[index])




def display_signal_timer_and_vehicle_count_for_each_signal(intersection :int, signal_number:int , signal_texts : list ):
        signal_texts[signal_number] = font.render(str(GD.intersections[intersection].signals[signal_number].signal_text), True, GD.white, GD.black)
        screen.blit(signal_texts[signal_number], GD.intersections[intersection].signal_timer_coordinates[signal_number])
        
        displayText = GD.crossed[intersection][GD.direction_numbers[signal_number]]['crossed']
        #displayText = GD.vehicles_[GD.direction_numbers[signal_number]]['crossed']
        GD.intersections[intersection].vehicle_count_texts[signal_number] = font.render(str(displayText), True, GD.black, GD.white)
        screen.blit(GD.intersections[intersection].vehicle_count_texts[signal_number], GD.intersections[intersection].vehicle_count_coordinates[signal_number])
        

def display_the_vehicles():
    for vehicle in sim.simulation:
        #screen.blit(vehicle.current_image, [vehicle.x, vehicle.y])
        vehicle.move_(screen)


def display_time_elapsed():
    algorithm_activity = 'OFF'
    if(GD.algorithm_active):
        algorithm_activity = 'ON'
    time_elapsed_text = font.render(f"Algorithm Activity Status  : {algorithm_activity} ", True, GD.black, GD.white)
    screen.blit(time_elapsed_text, (750, 20))
    time_elapsed_text = font.render(("Time Elapsed: " + str(GD.time_elapsed)), True, GD.black, GD.white)
    screen.blit(time_elapsed_text, (750, 50))
    


def signals_conroller(intersection):
            traffic_sign_arrow_images = []

            for dir in GD.direction_numbers.values():
                traffic_sign_arrow_images.append(pygame.image.load(f'images/traffic_signs/{dir}.png'))
            
            for i,coordinate in enumerate(GD.intersections[intersection].traffic_sign_arrow_coordinates):
                screen.blit(traffic_sign_arrow_images[i], (coordinate[0], coordinate[1]))



            for i in range(0, GD.intersections[intersection].number_of_signals):
                if(i == GD.intersections[intersection].current_green):
                    if(GD.intersections[intersection].current_yellow == 1):
                        GD.intersections[intersection].signals[i].signal_text = GD.intersections[intersection].signals[i].yellow
                        turn_signal_on(intersection ,signal_img=GD.yellow_signal_img, index=i)

                        
                    else:
                        GD.intersections[intersection].signals[i].signal_text = GD.intersections[intersection].signals[i].green
                        if(GD.intersections[intersection].signals[i].green <= 6 and GD.intersections[intersection].signals[i].green > 0 and GD.intersections[intersection].signals[i].green % 2 == 0):
                            turn_signal_on(intersection ,signal_img = GD.non_signal, index=i)
                            
                        elif(GD.intersections[intersection].signals[i].green <= 6 and GD.intersections[intersection].signals[i].green > 0 and GD.intersections[intersection].signals[i].green % 2 == 1):
                            turn_signal_on(intersection ,signal_img = GD.green_signal, index=i)
                        
                        else :
                            turn_signal_on(intersection ,signal_img = GD.green_signal, index=i)
        
                else:
                    # if(GD.intersections[intersection].signals[i].red  < 5 and i == GD.intersections[intersection].next_green):
                    #     GD.intersections[intersection].signals[i].signal_text = GD.intersections[intersection].signals[i].red 
                    # elif(i != GD.intersections[intersection].next_green or i != GD.intersections[intersection].current_green):
                    if(i != GD.intersections[intersection].current_green):
                        GD.intersections[intersection].signals[i].signal_text = ""
                    turn_signal_on(intersection , signal_img = GD.red_signal_img, index=i)
                

            signal_texts = ["", "", "", ""]
            for i in range(0, GD.intersections[intersection].number_of_signals):
                display_signal_timer_and_vehicle_count_for_each_signal(intersection ,signal_number = i , signal_texts = signal_texts)



    
def output():
    path , current_time = fc.create_directory()
    fc.create_xlsx_file()
    for vehicle in sim.simulation:
        data = { 
            'vehicle_type':vehicle.vehicle_class, 
            'vehicle_speed_avg':vehicle.speed_avg
            }
        fc.append_dict_to_xlsx( filename= 'vehicle_data.xlsx' , data=data  )               
    # Plot the average speeds for the specified vehicle types
    fc.plot_average_speeds_for_each_vehicle_type()
    fc.plot_vehicle_average_speed()
    pdf.create_report(path , current_time)
   

def to_percent(fraction):
    percent = int(round(fraction * 100))
    return f"{percent}%" , percent

def create_text(displayText , position, font_size):
    # Create the font object with the specified size
    font = pygame.font.Font(None, font_size)

    # Create the text surface
    text_surface = font.render(displayText, True, GD.white)

    # Get the rectangle for the text surface
    text_rect = text_surface.get_rect()

    # Set the position of the text rectangle
    text_rect.center = position #( 550,390)

    # Draw the text to the screen
    screen.blit(text_surface, text_rect) 



class Main:
    algorithm_activity = fc.read_xlsx_file_for_algo()
    if( algorithm_activity == 'true'):
        GD.algorithm_active = True

    GD.vehicles_generating  = fc.read_xlsx_file(directory = 'configuration' , filename = 'vehicles_data.xlsx',column='generating_number')
    GD.vehicles_weight      = fc.read_xlsx_file(directory = 'configuration' , filename = 'vehicles_data.xlsx',column='weight')
    GD.speeds               = fc.read_xlsx_file(directory = 'configuration' , filename = 'vehicles_data.xlsx',column='speed')
   
    cars_number:int = 0
    for v in GD.vehicles_generating.values():
        cars_number += v
    GD.cars_number = cars_number
    run_thread("generateVehicles" ,sim.generate_vehicle)
 
    while(GD.cars_number > 0):
        screen.blit(GD.loading, (0, 0))
        
        # Set the font and font size
        font = pygame.font.Font(None, 36)
        displayText,percent =to_percent((cars_number - GD.cars_number ) / cars_number)
        
        if(percent < 60):
            screen.blit(GD.red_signal_img_88, (350, 300))
        elif(percent >= 60 and percent < 90 ):
            create_text('Get Ready!' , ( 560,100) ,50)
            screen.blit(GD.yellow_signal_img_88, (350, 300))
        elif(percent >= 90 ):
            create_text('Go!' , ( 580,100) ,50)
            screen.blit(GD.green_signal_88 , (350, 300))

        
        create_text(displayText , ( 550,390) ,32)
        
        pygame.display.update()   

    #########################################################################################################################
    ####################################################    Threads   #######################################################
    #########################################################################################################################
    run_thread(thread_name="simulationTime" ,thread_target=sim.simulation_time)
    run_thread("initialization" ,sim.initialize)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if(GD.time_elapsed == GD.sim_time-2):
            output()
            sys.exit()
            
        
       
    #########################################################################################################################
    #######################################      Display Background In Simulation     #######################################
    #########################################################################################################################
        screen.blit(GD.background_white, (0, 0))
        screen.blit(GD.background, (150, 0))   
        #mouse coordination
        # mousex, mousey = pygame.mouse.get_pos()
        # print(f"{mousex} , {mousey}")

    #########################################################################################################################
    #######################################  display signal and set timer according   #######################################
    #######################################  to current status: green, yello, or red  #######################################
    #########################################################################################################################
        run_thread(thread_name="FGKJ signals_conroller" ,thread_target=signals_conroller,args=(GD.FGKJ,)).join()
        run_thread(thread_name="NOSR signals_conroller" ,thread_target=signals_conroller,args=(GD.NOSR,)).join()
    
        
        display_time_elapsed()

        display_the_vehicles()
        pygame.display.update()



