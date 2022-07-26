import threading
import pygame
import Simulation as sim
import sys
import GlobalData as GD

def run_thread(thread_name , thread_target):
    thread = threading.Thread(name=thread_name, target=thread_target, args=())
    thread.daemon = True
    thread.start()

class Main:
    run_thread("simulationTime" ,sim.simulationTime)
    run_thread("initialization" ,sim.initialize)
    run_thread("generateVehicles" ,sim.generateVehicles)
   
    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/mod_int.png')
    screen = pygame.display.set_mode(GD.screenSize)
    pygame.display.set_caption("SIMULATION")
    font = pygame.font.Font(None, GD.fontSize)
   

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (0, 0))   # display background in simulation
        # print(pygame.mouse.get_pos())
        # display signal and set timer according to current status: green, yello, or red
        for i in range(0, GD.noOfSignals):
            if(i == GD.currentGreen):
                if(GD.currentYellow == 1):
                    if(GD.signals[i].yellow == 0):
                        GD.signals[i].signalText = "STOP"
                    else:
                        GD.signals[i].signalText = GD.signals[i].yellow
                    screen.blit(GD.yellowSignal, GD.signalCoods[i])
                else:
                    GD.signals[i].signalText = GD.signals[i].green
                    if(GD.signals[i].green <= 6 and GD.signals[i].green > 0 and GD.signals[i].green % 2 == 0):
                        screen.blit(GD.nonSignal, GD.signalCoods[i])
                    elif(GD.signals[i].green <= 6 and GD.signals[i].green > 0 and GD.signals[i].green % 2 == 1):
                        screen.blit(GD.greenSignal, GD.signalCoods[i])
                    else :
                        if(GD.signals[i].green == 0):
                            GD.signals[i].signalText = "SLOW"
                        screen.blit(GD.greenSignal, GD.signalCoods[i])
            else:
                if(GD.signals[i].red <= 10):
                    if(GD.signals[i].red == 0):
                        GD.signals[i].signalText = "GO"
                    else:
                        GD.signals[i].signalText = GD.signals[i].red
                else:
                    GD.signals[i].signalText = ""
                screen.blit(GD.redSignal, GD.signalCoods[i])
        signalTexts = ["", "", "", ""]

        # display signal timer and vehicle count
        for i in range(0, GD.noOfSignals):
            signalTexts[i] = font.render(
                str(GD.signals[i].signalText), True, GD.white, GD.black)
            screen.blit(signalTexts[i], GD.signalTimerCoods[i])
            displayText = GD.vehicles[GD.directionNumbers[i]]['crossed']
            GD.vehicleCountTexts[i] = font.render(
                str(displayText), True, GD.black, GD.white)
            screen.blit(GD.vehicleCountTexts[i], GD.vehicleCountCoods[i])

        timeElapsedText = font.render(
            ("Time Elapsed: "+str(GD.timeElapsed)), True, GD.black, GD.white)
        screen.blit(timeElapsedText, (1100, 50))

        # display the vehicles
        for vehicle in sim.simulation:
            screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
            # vehicle.render(screen)
            vehicle.move()
        pygame.display.update()
