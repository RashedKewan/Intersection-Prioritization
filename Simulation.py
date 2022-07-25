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
from Vehicle import Vehicle
import GlobalData as GD


pygame.init()
simulation = pygame.sprite.Group()


# Initialization of signals with default values
def initialize():
    ts1 = TrafficSignal(0, GD.defaultYellow, GD.defaultGreen,
                        GD.defaultMinimum, GD.defaultMaximum)
    GD.signals.append(ts1)

    ts2 = TrafficSignal(ts1.red+ts1.yellow+ts1.green, GD.defaultYellow,
                        GD.defaultGreen, GD.defaultMinimum, GD.defaultMaximum)
    GD.signals.append(ts2)

    ts3 = TrafficSignal(GD.defaultRed, GD.defaultYellow,
                        GD.defaultGreen, GD.defaultMinimum, GD.defaultMaximum)
    GD.signals.append(ts3)

    ts4 = TrafficSignal(GD.defaultRed, GD.defaultYellow,
                        GD.defaultGreen, GD.defaultMinimum, GD.defaultMaximum)
    GD.signals.append(ts4)
    repeat()

# Set time according to formula


def increasVehicleCounter(vehicle):
    if(vehicle.crossed == 0):
        vclass = vehicle.vehicleClass
        if(vclass == GD.CAR):
            GD.noOfCars += 1
        elif(vclass == GD.BUS):
            GD.noOfBuses += 1
        elif(vclass == GD.TRUCK):
            GD.noOfTrucks += 1
        elif(vclass == GD.MOTORCYCLE):
            GD.noOfMotorcycle += 1


def readTextWithVoice(text, language):
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("detectingVehiclesSound.mp3")
    os.system("start detectingVehiclesSound.mp3")


def setTime():
    text = "detecting vehicles, " + \
        GD.directionNumbers[(GD.currentGreen+1) % GD.noOfSignals]
    language = 'en'
    #readTextWithVoice(text,language)
    #os.system("say detecting vehicles, " + GD.directionNumbers[(GD.currentGreen+1) % GD.noOfSignals])
    GD.noOfCars, GD.noOfBuses, GD.noOfTrucks, GD.noOfMotorcycle = 0, 0, 0, 0

    for i in range(1, 3):
        for j in range(len(GD.vehicles[GD.directionNumbers[GD.nextGreen]][i])):
            vehicle = GD.vehicles[GD.directionNumbers[GD.nextGreen]][i][j]
            increasVehicleCounter(vehicle)

    greenTime = math.ceil(((GD.noOfCars*GD.carTime) + (GD.noOfMotorcycle*GD.MotorcycleTime) + (
        GD.noOfBuses*GD.busTime) + (GD.noOfTrucks*GD.truckTime) + (GD.noOfMotorcycle*GD.MotorcycleTime))/(GD.noOfLanes+1))
    # greenTime = math.ceil((noOfVehicles)/noOfLanes)
    print('Green Time: ', greenTime)
    if(greenTime < GD.defaultMinimum):
        greenTime = GD.defaultMinimum
    elif(greenTime > GD.defaultMaximum):
        greenTime = GD.defaultMaximum
    # greenTime = random.randint(15,50)
    GD.signals[(GD.currentGreen+1) % (GD.noOfSignals)].green = greenTime


def repeat():
    # while the timer of current green signal is not zero
    while(GD.signals[GD.currentGreen].green > 0):
        # printStatus()
        updateValues()

        # set time of next green signal
        if(GD.signals[(GD.currentGreen+1) % (GD.noOfSignals)].red == GD.detectionTime):
            thread = threading.Thread(
                name="detection", target=setTime, args=())
            thread.daemon = True
            thread.start()
            # setTime()
        time.sleep(1)
        

    GD.currentYellow = 1   # set yellow signal on
    GD.vehicleCountTexts[GD.currentGreen] = "0"

    # reset stop coordinates of lanes and vehicles
    for i in range(0, 3):
        GD.stops[GD.directionNumbers[GD.currentGreen]
                 ][i] = GD.defaultStop[GD.directionNumbers[GD.currentGreen]]
        for vehicle in GD.vehicles[GD.directionNumbers[GD.currentGreen]][i]:
            vehicle.stop = GD.defaultStop[GD.directionNumbers[GD.currentGreen]]

    # while the timer of current yellow signal is not zero
    while(GD.signals[GD.currentGreen].yellow > 0):
        # printStatus()
        updateValues()
        time.sleep(1)
    GD.currentYellow = 0   # set yellow signal off

    # reset all signal times of current signal to default times
    GD.signals[GD.currentGreen].green = GD.defaultGreen
    GD.signals[GD.currentGreen].yellow = GD.defaultYellow
    GD.signals[GD.currentGreen].red = GD.defaultRed

    GD.currentGreen = GD.nextGreen  # set next signal as green signal
    # set next green signal
    GD.nextGreen = (GD.currentGreen+1) % GD.noOfSignals
    # set the red time of next to next signal as (yellow time + green time) of next signal
    GD.signals[GD.nextGreen].red = GD.signals[GD.currentGreen].yellow + \
        GD.signals[GD.currentGreen].green
    repeat()

# Print the signal timers on cmd


def printStatus():
    for i in range(0, GD.noOfSignals):
        if(i == GD.currentGreen):
            if(GD.currentYellow == 0):
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


def updateValues():
    for i in range(0, GD.noOfSignals):
        if(i == GD.currentGreen):
            if(GD.currentYellow == 0):
                GD.signals[i].green -= 1
                GD.signals[i].totalGreenTime += 1
            else:
                GD.signals[i].yellow -= 1
        else:
            GD.signals[i].red -= 1


def chooseDirection():
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


def generateVehicles():
    while(True):
        vehicle_type = random.randint(0, 3)

        # 0 in the white line
        # 1 street
        # 2 beside the yellow line
        lane_number = random.randint(0, 1)+1

        will_turn_right = 0
        will_turn_left = 0

        if(lane_number == 2):
            will_turn_right = checkIfWillTurn()
        elif (lane_number == 1):
            will_turn_left = checkIfWillTurn()

        direction_number = chooseDirection()
        Vehicle(lane_number, GD.vehicleTypes[vehicle_type], direction_number,
                GD.directionNumbers[direction_number], will_turn_right, will_turn_left)
        time.sleep(0.75)


def checkIfWillTurn():
    temp = random.randint(0, 3)
    if(temp < 2):
        return 1
    return 0


def simulationTime():
    while(True):
        GD.timeElapsed += 1
        time.sleep(1)
        if(GD.timeElapsed == GD.simTime):
            totalVehicles = 0
            print('Lane-wise Vehicle Counts')
            for i in range(GD.noOfSignals):
                print('Lane', i+1, ':',
                      GD.vehicles[GD.directionNumbers[i]]['crossed'])
                totalVehicles += GD.vehicles[GD.directionNumbers[i]]['crossed']
            print('Total vehicles passed: ', totalVehicles)
            print('Total time passed: ', GD.timeElapsed)
            print('No. of vehicles passed per unit time: ',
                  (float(totalVehicles)/float(GD.timeElapsed)))
            os._exit(1)
