import pygame
import time
from  threading import Thread


class Car:
    def __init__(self, WIN, x_position, y_position, image, speed=5, intersection_detected=False, can_move=True):
        self.WIN = WIN
        self.x_position = x_position
        self.y_position = y_position
        self.image = image
        self.speed = speed
        self.can_move = can_move
        self.intersection_detected = intersection_detected

    def draw(self):
        self.WIN.blit(self.image, (self.x_position, self.y_position))
    
    # move left to right
    def move_LR(self,PAUSE_MODE):
        # road_map[car.y_position-road.x_position][car.y_position-road.y_position] = 0
        if not PAUSE_MODE and self.can_move:
            if self.y_position < 400 and self.x_position == 120:
                self.y_position = self.y_position+self.speed

            elif self.y_position >= 400 and self.y_position < 490 and self.x_position < 240:
                self.x_position = self.x_position+5
                self.y_position = self.y_position+5

            elif self.x_position < 920 and self.y_position == 490 and not self.intersection_detected:
                self.x_position = self.x_position + self.speed

            elif self.y_position < 570 and self.x_position < 1000 and self.x_position >= 920:
                self.x_position = self.x_position + 5
                self.y_position = self.y_position + 5
                self.intersection_detected = True

            elif self.y_position <= 800 and self.x_position >= 1000:
                self.y_position = self.y_position+self.speed

            elif self.y_position >= 800 and self.y_position <= 900 and self.x_position > 900 and self.x_position <= 1000:
                self.y_position = self.y_position+5
                self.x_position = self.x_position-5

            elif self.y_position > 900 and self.x_position > 700:
                self.x_position = self.x_position-self.speed

            elif self.y_position > 790 and self.x_position > 590:
                self.x_position = self.x_position - 5
                self.y_position = self.y_position - 5

            elif self.y_position > 90 and self.intersection_detected:
                self.y_position = self.y_position - self.speed

            elif self.x_position > 520 and self.y_position > 20 and self.y_position <= 100:
                self.x_position = self.x_position - 5
                self.y_position = self.y_position - 5
                self.intersection_detected = False

            elif self.y_position <= 35 and self.x_position < 520 and self.x_position > 220:
                self.x_position = self.x_position - self.speed
            else:
                self.y_position = self.y_position+5
                self.x_position = self.x_position-5
            # overriding cars problem
            # if road_map[car.y_position-road.x_position + 80][car.y_position-road.y_position] == 1  and car.x_position+80 < 920:
            #        car.speed = 5
            # road_map[car.y_position -road.x_position][car.y_position-road.y_position] = 1
            # print('( ', car.x_position, ' , ', car.y_position, ' )')

        # detect car with red signal light
        if (445 == self.x_position) and (490 == self.y_position):
            p = Thread(target = self.countdown,args=(3,))
            p.start()
            #p.join()
        return self
    

        
    # counter for trafic signal
    def countdown(self, t):
        #t1 = int(str(t))
        self.can_move = False
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        self.can_move = True

    
