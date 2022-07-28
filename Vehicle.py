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
            coordination, dimension = 'x', -1 * (self.currentImage.get_rect().width + GD.gap)

        elif(direction == GD.LEFT):
            coordination, dimension = 'x', self.currentImage.get_rect().width + GD.gap

        elif(direction == GD.DOWN):
            coordination, dimension = 'y', -1 *(self.currentImage.get_rect().height + GD.gap)

        elif(direction == GD.UP):
            coordination, dimension = 'y', self.currentImage.get_rect().height + GD.gap
        self.setNewStartingAndStoppingCoordinate(coordination, dimension)

        # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
        if(len(GD.vehicles[direction][lane]) > 1 and GD.vehicles[direction][lane][self.index-1].crossed == 0):
            # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            self.stop = GD.vehicles[direction][lane][self.index-1].stop - GD.vehicles[direction][lane][self.index -1].currentImage.get_rect().width - GD.gap
        else:
            self.stop = GD.defaultStop[direction]
        sim.simulation.add(self)

    def setNewStartingAndStoppingCoordinate(self, coordination, newDimension):
        if(coordination == 'x'):
            GD.x[self.direction][self.lane] += newDimension
        else:
            GD.y[self.direction][self.lane] += newDimension
        GD.stops[self.direction][self.lane] += newDimension

    def render(self, screen):
        screen.blit(self.currentImage, (self.x, self.y))

    def turn(self, coordinate, coordinate_sign, oposit_cordinate_sign, x_steps ,y_steps,angel_sign, is_not_the_point_to_turn, is_the_environment_allows_to_move_on, the_rotation_has_end):
            if(is_not_the_point_to_turn):
                if(is_the_environment_allows_to_move_on):
                    if(coordinate == 'x'):
                        self.x += self.speed*coordinate_sign
                    elif(coordinate == 'y'):
                        self.y += self.speed*coordinate_sign
            else:
                if(self.turned == 0):
                    self.rotateAngle += GD.rotationAngle
                    self.currentImage = pygame.transform.rotate(self.originalImage, angel_sign*self.rotateAngle)
                    self.x += x_steps
                    self.y += y_steps
                    if(self.rotateAngle == 90):
                        self.turned = 1
                else:
                    if(the_rotation_has_end):
                        if(coordinate == 'x'):
                            self.y += self.speed*oposit_cordinate_sign
                            #if(self.x < GD.drive_orginizer[self.direction]-20):
                            #    self.x += -1*coordinate_sign
                        elif(coordinate == 'y'):
                            #if(self.y < GD.drive_orginizer[self.direction]-20):
                            #    self.y += -1*coordinate_sign*self.speed
                            self.x += self.speed*oposit_cordinate_sign
                            

    
    def applyMoving(self, coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right, y_steps_right, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right, coordinate_sign_left, oposit_cordinate_sign_left, x_steps_left, y_steps_left, is_not_the_point_to_turn_left, is_the_environment_allows_to_move_on_left, the_rotation_has_end_left, image_has_crossed_stop_line_now, it_can_move_straight):
        if(image_has_crossed_stop_line_now):
            self.crossed = 1
            GD.vehicles[self.direction]['crossed'] += 1

         ##### Turned right #####
        if(self.will_turn_right == 1):
           self.turn( coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right ,y_steps_right,-1, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right)

        ##### Turned left #####
        elif(self.will_turn_left == 1):
            self.turn( coordinate, coordinate_sign_left, oposit_cordinate_sign_left, x_steps_left ,y_steps_left,1, is_not_the_point_to_turn_left, is_the_environment_allows_to_move_on_left, the_rotation_has_end_left)
        else:
            if(it_can_move_straight):
                if(coordinate == 'x'):
                    self.x += self.speed*coordinate_sign_right
                    
                elif(coordinate == 'y'):
                    self.y += self.speed*coordinate_sign_right
                    


    def move(self):
        #####################################  RIGHT #####################################
        
        if(self.direction == GD.RIGHT):
            coordinate = 'x'
            
            coordinate_sign_right = 1
            oposit_cordinate_sign_right = 1
            x_steps_right = 2.2
            y_steps_right = 1.8
            is_not_the_point_to_turn_right = (self.crossed == 0) or (self.x + self.currentImage.get_rect().width < GD.directly[self.direction][coordinate])
            is_the_environment_allows_to_move_on_right = (self.x+self.currentImage.get_rect().width <= self.stop or (GD.currentGreen == 0 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x+self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)
            the_rotation_has_end_right = self.index == 0 or self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2) or self.x+self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2)
           
            coordinate_sign_left = 1
            oposit_cordinate_sign_left = -1
            x_steps_left = 2.2
            y_steps_left = -1.8
            is_not_the_point_to_turn_left = (self.crossed == 0) or (self.x + self.currentImage.get_rect().width < GD.mid[self.direction][coordinate])
            is_the_environment_allows_to_move_on_left = (self.x+self.currentImage.get_rect().width <= self.stop or (GD.currentGreen == 0 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x+self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))
            the_rotation_has_end_left = (self.index == 0 )or (self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2)) or (self.x+self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2))
           
            image_has_crossed_stop_line_now = (self.crossed == 0 )and (self.x + self.currentImage.get_rect().width > GD.stopLines[self.direction])
            it_can_move_straight = ((self.x+self.currentImage.get_rect().width <= self.stop) or (self.crossed == 1 )or (GD.currentGreen == 0 and GD.currentYellow == 0)) and ((self.index == 0) or (self.x +self.currentImage.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2)) or ((GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)))
           
        #####################################  DOWN #####################################
        elif(self.direction == GD.DOWN):
            coordinate = 'y'
            
            coordinate_sign_right = 1
            oposit_cordinate_sign_right = -1
            x_steps_right = -2.5
            y_steps_right = 2.2
            is_not_the_point_to_turn_right = (self.crossed == 0) or (self.y+self.currentImage.get_rect().height < GD.directly[self.direction][coordinate])
            is_the_environment_allows_to_move_on_right = ((self.y+self.currentImage.get_rect().height <= self.stop or (GD.currentGreen == 1 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))
            the_rotation_has_end_right = (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or self.y < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2))
           
            coordinate_sign_left = 1
            oposit_cordinate_sign_left = 1
            x_steps_left = 2.5
            y_steps_left = 2
            is_not_the_point_to_turn_left = (self.crossed == 0) or (self.y+self.currentImage.get_rect().height  < GD.mid[self.direction][coordinate])
            is_the_environment_allows_to_move_on_left = ((self.y+self.currentImage.get_rect().height <= self.stop or (GD.currentGreen == 1 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))
            the_rotation_has_end_left = (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or self.y < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2))
           
            image_has_crossed_stop_line_now = (self.crossed == 0 and self.y+self.currentImage.get_rect().height > GD.stopLines[self.direction])
            it_can_move_straight = ((self.y+self.currentImage.get_rect().height <= self.stop or self.crossed == 1 or (GD.currentGreen == 1 and GD.currentYellow == 0)) and (self.index == 0 or self.y+self.currentImage.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)))
          
        #####################################  LEFT #####################################
        elif(self.direction == GD.LEFT):  
            coordinate = 'x'
            
            coordinate_sign_right = -1
            oposit_cordinate_sign_right = -1
            x_steps_right = -1.5
            y_steps_right = -2.5
            is_not_the_point_to_turn_right = (self.crossed == 0) or (self.x > GD.directly[self.direction][coordinate])
            is_the_environment_allows_to_move_on_right =((self.x >= self.stop or (GD.currentGreen == 2 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))
            the_rotation_has_end_right = (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.gap2))
           
            coordinate_sign_left = -1
            oposit_cordinate_sign_left = 1
            x_steps_left = -1.8
            y_steps_left = 2.5
            is_not_the_point_to_turn_left = (self.crossed == 0) or (self.x > GD.mid[self.direction][coordinate])
            is_the_environment_allows_to_move_on_left = ((self.x >= self.stop or (GD.currentGreen == 2 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))
            the_rotation_has_end_left = True
           
            image_has_crossed_stop_line_now = (self.crossed == 0 and self.x < GD.stopLines[self.direction])
            it_can_move_straight = ((self.x >= self.stop or self.crossed == 1 or (GD.currentGreen == 2 and GD.currentYellow == 0)) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)))
          
        #####################################  UP #####################################
        elif(self.direction == GD.UP):   
            coordinate = 'y'
            
            coordinate_sign_right = -1
            oposit_cordinate_sign_right = 1
            x_steps_right = 1
            y_steps_right = -1
            is_not_the_point_to_turn_right = (self.crossed == 0) or (self.y > GD.directly[self.direction][coordinate])
            is_the_environment_allows_to_move_on_right =((self.y >= self.stop or (GD.currentGreen == 3 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().height + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))
            the_rotation_has_end_right = (self.index == 0 or self.x < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width - GD.gap2) or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.gap2))
           
            coordinate_sign_left = -1
            oposit_cordinate_sign_left = -1
            x_steps_left = -1.8
            y_steps_left = -2.5
            is_not_the_point_to_turn_left = (self.crossed == 0) or (self.y > GD.mid[self.direction][coordinate])
            is_the_environment_allows_to_move_on_left = ((self.y >= self.stop or (GD.currentGreen == 3 and GD.currentYellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().height + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index-1].turned == 1))
            the_rotation_has_end_left = True
           
            image_has_crossed_stop_line_now = (self.crossed == 0 and self.y < GD.stopLines[self.direction])
            it_can_move_straight =((self.y >= self.stop or self.crossed == 1 or (GD.currentGreen == 3 and GD.currentYellow == 0)) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().height + GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index-1].turned == 1)))
        
        self.applyMoving(coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right, y_steps_right, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right, coordinate_sign_left,oposit_cordinate_sign_left, x_steps_left, y_steps_left, is_not_the_point_to_turn_left, is_the_environment_allows_to_move_on_left, the_rotation_has_end_left, image_has_crossed_stop_line_now, it_can_move_straight)

