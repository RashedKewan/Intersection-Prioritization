import pygame
import Simulation as sim
import GlobalData as GD


class VehicleClass(pygame.sprite.Sprite):
    flag=False
    def __init__(self, lane : int , vehicle_class : str, direction : str, will_turn_right : bool , will_turn_left : bool ):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicle_class = vehicle_class
        self.speed = GD.speeds[vehicle_class]
        self.direction = direction
        self.x = GD.x[direction][lane]
        self.y = GD.y[direction][lane]
        self.crossed = 0
        self.will_turn_right = will_turn_right
        self.will_turn_left = will_turn_left
        self.turned = 0
        self.rotate_angle = 0
        GD.vehicles[direction][lane].append(self)
        self.index = len(GD.vehicles[direction][lane]) - 1
        path = f"images//{direction}//{vehicle_class}.png"
        self.original_image = pygame.image.load(path)
        self.current_image = pygame.image.load(path)

        # Set new starting and stopping coordinate
        coordination, dimension = self.get_coordination_dimension_accorfing_to_direction(self.direction)
        self.set_new_starting_and_stopping_coordinate(coordination, dimension)

        # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
        if(len(GD.vehicles[direction][lane]) > 1 and GD.vehicles[direction][lane][self.index-1].crossed == 0):
            # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            self.stop = GD.vehicles[direction][lane][self.index-1].stop - GD.vehicles[direction][lane][self.index -1].current_image.get_rect().width - GD.gap
        else:
            self.stop = GD.default_stop[direction]
        sim.simulation.add(self)



    def set_new_starting_and_stopping_coordinate(self, coordination : str, new_dimension:int):
        if(coordination == 'x'):
            GD.x[self.direction][self.lane] += new_dimension
        else:
            GD.y[self.direction][self.lane] += new_dimension
        GD.stops[self.direction][self.lane] += new_dimension



    def get_coordination_dimension_accorfing_to_direction(self,direction:str):
        coordination, dimension = '', 0
        if(direction == GD.RIGHT):
            coordination, dimension = 'x', -1 * (self.current_image.get_rect().width + GD.gap)

        elif(direction == GD.LEFT):
            coordination, dimension = 'x', self.current_image.get_rect().width + GD.gap

        elif(direction == GD.DOWN):
            coordination, dimension = 'y', -1 *(self.current_image.get_rect().height + GD.gap)

        elif(direction == GD.UP):
            coordination, dimension = 'y', self.current_image.get_rect().height + GD.gap
        return coordination, dimension

    def render(self, screen):
        screen.blit(self.current_image, (self.x, self.y))



    def turn(self, coordinate : str , coordinate_sign : int , oposit_cordinate_sign : int, x_steps : int ,y_steps : int ,angel_sign : int, is_not_the_point_to_turn : bool, is_the_environment_allows_to_move_on : bool , the_rotation_has_end : bool):
            global flag
            dir=''
            if(is_not_the_point_to_turn):
                if(is_the_environment_allows_to_move_on):
                    if(coordinate == 'x'):
                        self.x += self.speed*coordinate_sign
                    elif(coordinate == 'y'):
                        self.y += self.speed*coordinate_sign
            else:
                if(self.turned == 0):
                    self.handle_turned_equal_zero(angel_sign = angel_sign, x_steps = x_steps, y_steps = y_steps)

                else:
                    if(the_rotation_has_end):
                        if angel_sign == -1:
                            dir = self.get_direction_after_rotate('right')
                        elif angel_sign == 1:
                            dir = self.get_direction_after_rotate('left')
                        #print(f'dir = {dir}')
                        #self.get_lane_coordinate_after_rotation(dir,coordinate)
                        if(coordinate == 'x'):
                            self.y += self.speed*oposit_cordinate_sign
                            #if(self.x > GD.directly[dir]['y']+20):
                            #    self.x += -1*coordinate_sign*0.5
                            #    print('-------------->')
                        elif(coordinate == 'y'):
                            self.x += self.speed*oposit_cordinate_sign

    def handle_turned_equal_zero(self, angel_sign:int, x_steps:int, y_steps:int):
        self.rotate_angle += GD.rotation_angle
        self.current_image = pygame.transform.rotate(self.original_image, angel_sign * self.rotate_angle)
        self.x += x_steps
        self.y += y_steps
        if (self.rotate_angle == 90):
            self.turned = 1

    def get_oposite_direction(self,direction:str)->str:# no need
        if direction == GD.UP:
            return GD.DOWN
        if direction == GD.DOWN:
            return GD.UP
        if direction == GD.LEFT:
            return GD.RIGHT
        return GD.LEFT


    # weight of vehicle  = GD.vehiclesWeight[self.vehicleClass]

    def get_lane_coordinate_after_rotation(self ,dir, coordinate ):# no need
        direction = dir
        print('{} == {} : {}'.format(self.direction , dir , self.direction == dir))
        print('x befor : {}'.format(self.x))
        if coordinate == 'x':
            if direction == GD.UP:
                self.x = GD.drive_orginizer[GD.DOWN]
            elif direction == GD.DOWN:
                self.x = GD.drive_orginizer[GD.UP]
            elif direction == GD.LEFT:
                self.x = GD.drive_orginizer[GD.RIGHT]
            elif direction == GD.RIGHT:
                self.x = GD.drive_orginizer[GD.LEFT]
        print('x after : {}'.format(self.x))
        if coordinate == 'y':
            if direction == GD.UP:
                self.y = GD.drive_orginizer[GD.DOWN]
            elif direction == GD.DOWN:
                self.y = GD.drive_orginizer[GD.UP]
            elif direction == GD.LEFT:
                self.y = GD.drive_orginizer[GD.RIGHT]
            elif direction == GD.RIGHT:
                self.y = GD.drive_orginizer[GD.LEFT]


    def get_direction_after_rotate(self , rotate_to : str) -> str:
        direction = self.direction
        new_direction = ''

        if direction == GD.RIGHT:
            if rotate_to == 'left':
                new_direction = GD.UP
            elif rotate_to == 'right':
                new_direction = GD.DOWN

        elif direction == GD.LEFT:
            if rotate_to == 'left':
                new_direction = GD.DOWN
            elif rotate_to == 'right':
                new_direction = GD.UP

        elif direction == GD.DOWN:
            if rotate_to == 'left':
                new_direction = GD.RIGHT
            elif rotate_to == 'right':
                new_direction = GD.LEFT

        elif direction == GD.UP:
            if rotate_to == 'left':
                new_direction = GD.LEFT
            elif rotate_to == 'right':
                new_direction = GD.RIGHT

        return new_direction

    
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
            is_not_the_point_to_turn_right = (self.crossed == 0) or (self.x + self.current_image.get_rect().width < GD.directly[self.direction][coordinate])
            is_the_environment_allows_to_move_on_right = (self.x + self.current_image.get_rect().width <= self.stop or (GD.current_green == 0 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.x + self.current_image.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index - 1].x - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1)
            the_rotation_has_end_right = self.index == 0 or self.y+self.current_image.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2) or self.x+self.current_image.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2)
           
            coordinate_sign_left = 1
            oposit_cordinate_sign_left = -1
            x_steps_left = 2.2
            y_steps_left = -1.8
            is_not_the_point_to_turn_left = (self.crossed == 0) or (self.x + self.current_image.get_rect().width < GD.mid[self.direction][coordinate])
            is_the_environment_allows_to_move_on_left = (self.x + self.current_image.get_rect().width <= self.stop or (GD.current_green == 0 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.x + self.current_image.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index - 1].x - GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
            the_rotation_has_end_left = (self.index == 0 )or (self.y+self.current_image.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2)) or (self.x+self.current_image.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2))
           
            image_has_crossed_stop_line_now = (self.crossed == 0 )and (self.x + self.current_image.get_rect().width > GD.stop_lines[self.direction])
            it_can_move_straight = ((self.x+self.current_image.get_rect().width <= self.stop) or (self.crossed == 1 ) or (GD.current_green == 0 and GD.current_yellow == 0)) and ((self.index == 0) or (self.x + self.current_image.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index - 1].x - GD.gap2)) or ((GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1)))
           
        #####################################  DOWN #####################################
        elif(self.direction == GD.DOWN):
            coordinate = 'y'
            
            coordinate_sign_right = 1
            oposit_cordinate_sign_right = -1
            x_steps_right = -2.5
            y_steps_right = 2.2
            is_not_the_point_to_turn_right = (self.crossed == 0) or (self.y+self.current_image.get_rect().height < GD.directly[self.direction][coordinate])
            is_the_environment_allows_to_move_on_right = ((self.y + self.current_image.get_rect().height <= self.stop or (GD.current_green == 1 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.y + self.current_image.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index - 1].y - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
            the_rotation_has_end_right = (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].current_image.get_rect().width + GD.gap2) or self.y < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2))
           
            coordinate_sign_left = 1
            oposit_cordinate_sign_left = 1
            x_steps_left = 2.5
            y_steps_left = 2
            is_not_the_point_to_turn_left = (self.crossed == 0) or (self.y+self.current_image.get_rect().height  < GD.mid[self.direction][coordinate])
            is_the_environment_allows_to_move_on_left = ((self.y + self.current_image.get_rect().height <= self.stop or (GD.current_green == 1 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.y + self.current_image.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index - 1].y - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
            the_rotation_has_end_left = (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].current_image.get_rect().width + GD.gap2) or self.y < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2))
           
            image_has_crossed_stop_line_now = (self.crossed == 0 and self.y+self.current_image.get_rect().height > GD.stop_lines[self.direction])
            it_can_move_straight = ((self.y + self.current_image.get_rect().height <= self.stop or self.crossed == 1 or (GD.current_green == 1 and GD.current_yellow == 0)) and (self.index == 0 or self.y + self.current_image.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index - 1].y - GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1)))
          
        #####################################  LEFT #####################################
        elif(self.direction == GD.LEFT):  
            coordinate = 'x'
            
            coordinate_sign_right = -1
            oposit_cordinate_sign_right = -1
            x_steps_right = -1.5
            y_steps_right = -2.5
            is_not_the_point_to_turn_right = (self.crossed == 0) or (self.x > GD.directly[self.direction][coordinate])
            is_the_environment_allows_to_move_on_right =((self.x >= self.stop or (GD.current_green == 2 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index - 1].x + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().width + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
            the_rotation_has_end_right = (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].current_image.get_rect().width + GD.gap2) or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.gap2))
           
            coordinate_sign_left = -1
            oposit_cordinate_sign_left = 1
            x_steps_left = -1.8
            y_steps_left = 2.5
            is_not_the_point_to_turn_left = (self.crossed == 0) or (self.x > GD.mid[self.direction][coordinate])
            is_the_environment_allows_to_move_on_left = ((self.x >= self.stop or (GD.current_green == 2 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index - 1].x + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().width + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
            the_rotation_has_end_left = True
           
            image_has_crossed_stop_line_now = (self.crossed == 0 and self.x < GD.stop_lines[self.direction])
            it_can_move_straight = ((self.x >= self.stop or self.crossed == 1 or (GD.current_green == 2 and GD.current_yellow == 0)) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index - 1].x + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().width + GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1)))
          
        #####################################  UP #####################################
        elif(self.direction == GD.UP):   
            coordinate = 'y'
            
            coordinate_sign_right = -1
            oposit_cordinate_sign_right = 1
            x_steps_right = 1
            y_steps_right = -1
            is_not_the_point_to_turn_right = (self.crossed == 0) or (self.y > GD.directly[self.direction][coordinate])
            is_the_environment_allows_to_move_on_right =((self.y >= self.stop or (GD.current_green == 3 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index - 1].y + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().height + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
            the_rotation_has_end_right = (self.index == 0 or self.x < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.vehicles[self.direction][self.lane][self.index-1].current_image.get_rect().width - GD.gap2) or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.gap2))
           
            coordinate_sign_left = -1
            oposit_cordinate_sign_left = -1
            x_steps_left = -1.8
            y_steps_left = -2.5
            is_not_the_point_to_turn_left = (self.crossed == 0) or (self.y > GD.mid[self.direction][coordinate])
            is_the_environment_allows_to_move_on_left = ((self.y >= self.stop or (GD.current_green == 3 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index - 1].y + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().height + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
            the_rotation_has_end_left = True
           
            image_has_crossed_stop_line_now = (self.crossed == 0 and self.y < GD.stop_lines[self.direction])
            it_can_move_straight =((self.y >= self.stop or self.crossed == 1 or (GD.current_green == 3 and GD.current_yellow == 0)) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index - 1].y + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().height + GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1)))
        
        self.applyMoving(coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right, y_steps_right, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right, coordinate_sign_left,oposit_cordinate_sign_left, x_steps_left, y_steps_left, is_not_the_point_to_turn_left, is_the_environment_allows_to_move_on_left, the_rotation_has_end_left, image_has_crossed_stop_line_now, it_can_move_straight)

