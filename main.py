import threading
import pygame
import Simulation as sim
import sys
import GlobalData as GD

def run_thread(thread_name:str , thread_target):
    thread = threading.Thread(name=thread_name, target=thread_target, args=())
    thread.daemon = True
    thread.start()


screen = pygame.display.set_mode(GD.screenSize)
pygame.display.set_caption("SIMULATION")
font = pygame.font.Font(None, GD.fontSize)

def turn_on(signal, index:int):
    screen.blit(signal, GD.signalCoods[index])

class Main:
    #########################################################################################################################
    ####################################################    Threads   #######################################################
    #########################################################################################################################
    run_thread(thread_name="simulationTime" ,thread_target=sim.simulationTime)
    run_thread("initialization" ,sim.initialize)
    run_thread("generateVehicles" ,sim.generateVehicles)


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

        for i in range(0, GD.no_of_signals):
            if(i == GD.current_green):
                if(GD.current_yellow == 1):
                    #if(GD.signals[i].yellow == 0):
                    #    GD.signals[i].signalText = "STOP"
                    #else:
                    GD.signals[i].signalText = GD.signals[i].yellow
                    turn_on(signal=GD.yellow_signal_img, index=i)

                    
                else:
                    GD.signals[i].signalText = GD.signals[i].green
                    if(GD.signals[i].green <= 6 and GD.signals[i].green > 0 and GD.signals[i].green % 2 == 0):
                        turn_on(GD.nonSignal, i)
                        
                    elif(GD.signals[i].green <= 6 and GD.signals[i].green > 0 and GD.signals[i].green % 2 == 1):
                        turn_on(GD.greenSignal, i)
                       
                    else :
                        #if(GD.signals[i].green == 0):
                        #    GD.signals[i].signalText = "SLOW"
                        turn_on(GD.greenSignal, i)
    
            else:
                if(GD.signals[i].red <= 10):
                    GD.signals[i].signalText = GD.signals[i].red 
                else:
                    GD.signals[i].signalText = ""
                turn_on(GD.red_signal_img, i)
               
        signalTexts = ["", "", "", ""]

        # display signal timer and vehicle count
        for i in range(0, GD.no_of_signals):
            signalTexts[i] = font.render(str(GD.signals[i].signalText), True, GD.white, GD.black)
            screen.blit(signalTexts[i], GD.signalTimerCoods[i])
            displayText = GD.vehicles[GD.directionNumbers[i]]['crossed']
            GD.vehicleCountTexts[i] = font.render(str(displayText), True, GD.black, GD.white)
            screen.blit(GD.vehicleCountTexts[i], GD.vehicleCountCoods[i])

        timeElapsedText = font.render(("Time Elapsed: " + str(GD.time_elapsed)), True, GD.black, GD.white)
        screen.blit(timeElapsedText, (1100, 50))

        # display the vehicles
        for vehicle in sim.simulation:
            screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
            vehicle.move()
        pygame.display.update()
