import pygame
import Simulation as sim
import GlobalData as GD


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, will_turn_right, will_turn_left):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = GD.speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = GD.x[direction][lane]
        self.y = GD.y[direction][lane]
        self.crossed = 0
        self.will_turn_right = will_turn_right
        self.will_turn_left = will_turn_left
        self.turned = 0
        self.rotateAngle = 0
        GD.vehicles[direction][lane].append(self)
        # self.stop = stops[direction][lane]
        self.index = len(GD.vehicles[direction][lane]) - 1
        path = "images/" + direction + "/" + vehicleClass + ".png"
        self.originalImage = pygame.image.load(path)
        self.currentImage = pygame.image.load(path)

        # Set new starting and stopping coordinate
        coordination, dimension = '', 0
        if(direction == GD.RIGHT):
            coordination, dimension = 'x', -1 * \
                (self.currentImage.get_rect().width + GD.gap)

        elif(direction == GD.LEFT):
            coordination, dimension = 'x', self.currentImage.get_rect().width + GD.gap

        elif(direction == GD.DOWN):
            coordination, dimension = 'y', -1 * \
                (self.currentImage.get_rect().height + GD.gap)

        elif(direction == GD.UP):
            coordination, dimension = 'y', self.currentImage.get_rect().height + GD.gap
        self.setNewStartingAndStoppingCoordinate(coordination, dimension)

        # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
        if(len(GD.vehicles[direction][lane]) > 1 and GD.vehicles[direction][lane][self.index-1].crossed == 0):
            # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            self.stop = GD.vehicles[direction][lane][self.index-1].stop - \
                GD.vehicles[direction][lane][self.index -
                                             1].currentImage.get_rect().width - GD.gap
        else:
            self.stop = GD.defaultStop[direction]
        sim.simulation.add(self)
        """
        if(direction=='right'):
            if(len(GD.vehicles[direction][lane])>1 and GD.vehicles[direction][lane][self.index-1].crossed==0):    # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
                self.stop = GD.vehicles[direction][lane][self.index-1].stop - GD.vehicles[direction][lane][self.index-1].currentImage.get_rect().width - GD.gap         # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = GD.defaultStop[direction]
            # Set new starting and stopping coordinate
            temp = self.currentImage.get_rect().width + GD.gap    
            GD.x[direction][lane] -= temp
            GD.stops[direction][lane] -= temp
        elif(direction=='left'):
            if(len(GD.vehicles[direction][lane])>1 and GD.vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = GD.vehicles[direction][lane][self.index-1].stop + GD.vehicles[direction][lane][self.index-1].currentImage.get_rect().width + GD.gap
            else:
                self.stop = GD.defaultStop[direction]
            temp = self.currentImage.get_rect().width + GD.gap
            GD.x[direction][lane] += temp
            GD.stops[direction][lane] += temp
        elif(direction=='down'):
            if(len(GD.vehicles[direction][lane])>1 and GD.vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = GD.vehicles[direction][lane][self.index-1].stop - GD.vehicles[direction][lane][self.index-1].currentImage.get_rect().height - GD.gap
            else:
                self.stop = GD.defaultStop[direction]
            temp = self.currentImage.get_rect().height + GD.gap
            GD.y[direction][lane] -= temp
            GD.stops[direction][lane] -= temp
        elif(direction=='up'):
            if(len(GD.vehicles[direction][lane])>1 and GD.vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = GD.vehicles[direction][lane][self.index-1].stop + GD.vehicles[direction][lane][self.index-1].currentImage.get_rect().height + GD.gap
            else:
                self.stop = GD.defaultStop[direction]
            temp = self.currentImage.get_rect().height + GD.gap
            GD.y[direction][lane] += temp
            GD.stops[direction][lane] += temp
        sim.simulation.add(self)
        """

    def setNewStartingAndStoppingCoordinate(self, coordination, newDimension):
        if(coordination == 'x'):
            GD.x[self.direction][self.lane] += newDimension
        else:
            GD.y[self.direction][self.lane] += newDimension
        GD.stops[self.direction][self.lane] += newDimension

    def render(self, screen):
        screen.blit(self.currentImage, (self.x, self.y))


    def move(self):
        #####################################  RIGHT #####################################
        if(self.direction == GD.RIGHT):
            # if the image has crossed stop line now
            if(self.crossed == 0 and self.x+self.currentImage.get_rect().width > GD.stopLines[self.direction]):
                self.crossed = 1
                GD.vehicles[self.direction]['crossed'] += 1
         ##### Turned right #####
            if(self.will_turn_right == 1):
                if(self.crossed == 0 or self.x+self.currentImage.get_rect().width < GD.directly[self.direction]['x']):
                    if((self.x+self.currentImage.get_rect().width <= self.stop or (GD.currentGreen == 0 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x+self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x += self.speed
                else:
                    if(self.turned == 0):
                        self.rotateAngle += GD.rotationAngle
                        self.currentImage = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x += 2.2
                        self.y += 1.8
                        if(self.rotateAngle == 90):
                            self.turned = 1
                    else:
                        if(self.index == 0 or self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2) or self.x+self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2)):
                            self.y += self.speed

            ##### Turned left #####
            elif(self.will_turn_left == 1):
                if(self.crossed == 0 or self.x+self.currentImage.get_rect().width < GD.mid[self.direction]['x']):
                    if((self.x+self.currentImage.get_rect().width <= self.stop or (GD.currentGreen == 0 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x+self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x += self.speed
                else:
                    if(self.turned == 0):
                        self.rotateAngle += GD.rotationAngle
                        self.currentImage = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x += 2.2
                        self.y -= 1.8
                        if(self.rotateAngle == 90):
                            self.turned = 1
                    else:
                        if(self.index == 0 or self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2) or self.x+self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2)):
                            self.y -= self.speed
            else:
                if((self.x+self.currentImage.get_rect().width <= self.stop or self.crossed == 1 or (GD.currentGreen == 0 and GD.currentYellow == 0)) and (self.index == 0 or self.x+self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))):
                    # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
                    self.x += self.speed  # move the vehicle
        
        #####################################  DOWN #####################################
      
        elif(self.direction == GD.DOWN):
            if(self.crossed == 0 and self.y+self.currentImage.get_rect().height > GD.stopLines[self.direction]):
                self.crossed = 1
                GD.vehicles[self.direction]['crossed'] += 1
         ##### Turned right #####
            if(self.will_turn_right == 1):
                if(self.crossed == 0 or self.y+self.currentImage.get_rect().height < GD.directly[self.direction]['y']):
                    if((self.y+self.currentImage.get_rect().height <= self.stop or (GD.currentGreen == 1 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y += self.speed
                else:
                    if(self.turned == 0):
                        self.rotateAngle += GD.rotationAngle
                        self.currentImage = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x -= 2.5  # 2.5
                        self.y += 2.2  # 2.2
                        if(self.rotateAngle == 90):
                            self.turned = 1

                    else:
                        if(self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or self.y < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2)):
                            self.x -= self.speed
                            if self.y > 410:  # beside white line , direction : down -> left
                                self.y -= 2.2  # 2.2
            ##### Turned left #####
            elif(self.will_turn_left == 1):
                if(self.crossed == 0 or self.y+self.currentImage.get_rect().height < GD.mid[self.direction]['y']):
                    if((self.y+self.currentImage.get_rect().height <= self.stop or (GD.currentGreen == 1 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y += self.speed
                else:
                    if(self.turned == 0):
                        self.rotateAngle += GD.rotationAngle
                        self.currentImage = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x += 2.5  # 2.5
                        self.y += 2  # 2.2
                        if(self.rotateAngle == 90):
                            self.turned = 1

                    else:
                        if(self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or self.y < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2)):
                            self.x += self.speed

            else:
                if((self.y+self.currentImage.get_rect().height <= self.stop or self.crossed == 1 or (GD.currentGreen == 1 and GD.currentYellow == 0)) and (self.index == 0 or self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))):
                    self.y += self.speed

        #####################################  LEFT #####################################
        elif(self.direction == GD.LEFT):
            if(self.crossed == 0 and self.x < GD.stopLines[self.direction]):
                self.crossed = 1
                GD.vehicles[self.direction]['crossed'] += 1

         ##### Turned right #####
            if(self.will_turn_right == 1):
                if(self.crossed == 0 or self.x > GD.directly[self.direction]['x']):
                    if((self.x >= self.stop or (GD.currentGreen == 2 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x -= self.speed
                else:
                    if(self.turned == 0):
                        self.rotateAngle += GD.rotationAngle
                        self.currentImage = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x -= 1.5
                        self.y -= 2.5
                        if(self.rotateAngle == 90):
                            self.turned = 1
                    else:
                        if(self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.gap2)):
                            self.y -= self.speed

         ##### Turned left #####
            elif(self.will_turn_left == 1):
                if(self.crossed == 0 or self.x > GD.mid[self.direction]['x']):
                    if((self.x >= self.stop or (GD.currentGreen == 2 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.x -= self.speed
                else:
                    if(self.turned == 0):
                        self.rotateAngle += GD.rotationAngle
                        self.currentImage = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x -= 1.8
                        self.y += 2.5
                        if(self.rotateAngle == 90):
                            self.turned = 1
                    else:
                        # if(self.index == 0 or self.y >= (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or self.x >= (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.gap2)):
                        self.y += self.speed
            else:
                if((self.x >= self.stop or self.crossed == 1 or (GD.currentGreen == 2 and GD.currentYellow == 0)) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))):
                    # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
                    self.x -= self.speed  # move the vehicle

        #####################################  UP #####################################
        elif(self.direction == GD.UP):
            if(self.crossed == 0 and self.y < GD.stopLines[self.direction]):
                self.crossed = 1
                GD.vehicles[self.direction]['crossed'] += 1

            if(self.will_turn_right == 1):
                if(self.crossed == 0 or self.y > GD.directly[self.direction]['y']):
                    if((self.y >= self.stop or (GD.currentGreen == 3 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().height + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y -= self.speed
                else:
                    if(self.turned == 0):
                        self.rotateAngle += GD.rotationAngle
                        self.currentImage = pygame.transform.rotate(
                            self.originalImage, -self.rotateAngle)
                        self.x += 1
                        self.y -= 1
                        if(self.rotateAngle == 90):
                            self.turned = 1
                    else:
                        if(self.index == 0 or self.x < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width - GD.gap2) or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.gap2)):
                            self.x += self.speed

            elif(self.will_turn_left == 1):
                if(self.crossed == 0 or self.y > GD.mid[self.direction]['y']):
                    if((self.y >= self.stop or (GD.currentGreen == 3 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().height + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)):
                        self.y -= self.speed
                else:
                    if(self.turned == 0):
                        self.rotateAngle += GD.rotationAngle
                        self.currentImage = pygame.transform.rotate(
                            self.originalImage, self.rotateAngle)
                        self.x -= 1.8
                        self.y -= 2.5
                        if(self.rotateAngle == 90):
                            self.turned = 1
                    else:
                        # if(self.index == 0 or self.x < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width - GD.gap2) or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.gap2)):
                        self.x -= self.speed
            else:
                if((self.y >= self.stop or self.crossed == 1 or (GD.currentGreen == 3 and GD.currentYellow == 0)) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().height + GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))):
                    self.y -= self.speed
