import threading
import pygame
import Simulation as sim
import sys
import GlobalData as GD


class Main:
    thread4 = threading.Thread(
        name="simulationTime", target=sim.simulationTime, args=())
    thread4.daemon = True
    thread4.start()

    thread2 = threading.Thread(
        name="initialization", target=sim.initialize, args=())    # initialization
    thread2.daemon = True
    thread2.start()

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/mod_int.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    nonSignal = pygame.image.load('images/signals/non.png')
    font = pygame.font.Font(None, GD.fontSize)

    thread3 = threading.Thread(
        name="generateVehicles", target=sim.generateVehicles, args=())    # Generating vehicles
    thread3.daemon = True
    thread3.start()

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
                    screen.blit(yellowSignal, GD.signalCoods[i])
                else:
                    GD.signals[i].signalText = GD.signals[i].green
                    if(GD.signals[i].green <= 6 and GD.signals[i].green > 0 and GD.signals[i].green % 2 == 0):
                        screen.blit(nonSignal, GD.signalCoods[i])
                    elif(GD.signals[i].green <= 6 and GD.signals[i].green > 0 and GD.signals[i].green % 2 == 1):
                        screen.blit(greenSignal, GD.signalCoods[i])
                    else :
                        if(GD.signals[i].green == 0):
                            GD.signals[i].signalText = "SLOW"
                        #else:
                        #    GD.signals[i].signalText = GD.signals[i].green
                        screen.blit(greenSignal, GD.signalCoods[i])
            else:
                if(GD.signals[i].red <= 10):
                    if(GD.signals[i].red == 0):
                        GD.signals[i].signalText = "GO"
                    else:
                        GD.signals[i].signalText = GD.signals[i].red
                else:
                    GD.signals[i].signalText = "---"
                screen.blit(redSignal, GD.signalCoods[i])
        signalTexts = ["", "", "", ""]

        # display signal timer and vehicle count
        for i in range(0, GD.noOfSignals):
            signalTexts[i] = font.render(
                str(GD.signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], GD.signalTimerCoods[i])
            displayText = GD.vehicles[GD.directionNumbers[i]]['crossed']
            GD.vehicleCountTexts[i] = font.render(
                str(displayText), True, black, white)
            screen.blit(GD.vehicleCountTexts[i], GD.vehicleCountCoods[i])

        timeElapsedText = font.render(
            ("Time Elapsed: "+str(GD.timeElapsed)), True, black, white)
        screen.blit(timeElapsedText, (1100, 50))

        # display the vehicles
        for vehicle in sim.simulation:
            screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
            # vehicle.render(screen)
            vehicle.move()
        pygame.display.update()
