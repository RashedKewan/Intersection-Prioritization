import pygame
import Simulation as sim
import GlobalData as GD


class VehicleClass(pygame.sprite.Sprite):
    flag=False
    def __init__(self, lane : int , vehicle_class : str, direction : int, will_turn_right : bool , will_turn_left : bool ,x : int , y : int ):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicle_class = vehicle_class
        self.speed = GD.speeds[vehicle_class]
        self.direction = direction
        self.x = x #GD.streets[direction][lane]['x'][0]#GD.x[direction][lane]
        self.y = y #GD.streets[direction][lane]['y'][0]#GD.y[direction][lane]
        self.crossed = 0
        self.will_turn_right = will_turn_right
        self.will_turn_left = will_turn_left
        self.turned = 0
        self.rotate_angle = 0
        #GD.vehicles_[direction][lane].append(self)
        #self.index = len(GD.vehicles_[direction][lane]) - 1
        path = f"images//{direction}//{vehicle_class}.png"
        self.original_image = pygame.image.load(path)
        self.current_image = pygame.image.load(path)
        

        # # Set new starting and stopping coordinate
        # coordination, dimension = self.get_coordination_dimension_accorfing_to_direction(self.direction)
        # #self.set_new_starting_and_stopping_coordinate(coordination, dimension)

        # # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
        # if(len(GD.vehicles_[direction][lane]) > 1 and GD.vehicles_[direction][lane][self.index-1].crossed == 0):
        #     # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
        #     self.stop = GD.vehicles_[direction][lane][self.index-1].stop - GD.vehicles_[direction][lane][self.index -1].current_image.get_rect().width - GD.gap
        # else:
        #     self.stop = GD.default_stop[direction]
        sim.simulation.add(self)

#############################################################################################################################
   
    def print(self):
        print(f"\
            *********************************************\n \
            vehicle_class   : {self.vehicle_class} \n \
            lane            : {self.lane} \n \
            direction       : {self.direction}\n \
            will_turn_right : {self.will_turn_right} \n \
            will_turn_left  : {self.will_turn_left} \n \
            x               : {self.x}\n \
            y               : {self.y}\n \
            *********************************************\n\n")

#############################################################################################################################
   

    def set_new_starting_and_stopping_coordinate(self, coordination : str, new_dimension:int):
        if(coordination == 'x'):
            #GD.x[self.direction][self.lane] += new_dimension
            GD.streets[self.direction][self.lane]['x'][0]+= new_dimension
        else:
            #GD.y[self.direction][self.lane] += new_dimension
            GD.streets[self.direction][self.lane]['y'][0]+= new_dimension
        GD.stops[self.direction][self.lane] += new_dimension


#############################################################################################################################
   
   
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


#############################################################################################################################


    # def render(self, screen):
    #     screen.blit(self.current_image, (self.x, self.y))


#############################################################################################################################


    # def turn(self, coordinate : str , coordinate_sign : int , oposit_cordinate_sign : int, x_steps : int ,y_steps : int ,angel_sign : int, is_not_the_point_to_turn : bool, is_the_environment_allows_to_move_on : bool , the_rotation_has_end : bool)->bool:
    #         if(is_not_the_point_to_turn):
    #             if(is_the_environment_allows_to_move_on):
    #                 if(coordinate == 'x'):
    #                     self.x += self.speed*coordinate_sign
    #                 elif(coordinate == 'y'):
    #                     self.y += self.speed*coordinate_sign
    #         else:
    #             if(self.turned == 0):
    #                 self.handle_turned_equal_zero(angel_sign = angel_sign, x_steps = x_steps, y_steps = y_steps)
    #             else:
    #                 if(the_rotation_has_end):
    #                     # if(coordinate == 'x'):
    #                     #     self.y += self.speed*oposit_cordinate_sign
    #                     # elif(coordinate == 'y'):
    #                     #     self.x += self.speed*oposit_cordinate_sign
    #                     self.direction = GD.DOWN
    #                     if(self.lane == GD.CD):
    #                         self.lane = GD.D_F_
    #                     elif(self.lane == GD.KL):
    #                         self.lane = GD.L_N_
    #                     elif(self.lane == GD.ST):
    #                         self.lane = GD.T_V_
    #                     print('ooooooooo')
    #                     if( (self.direction == GD.DOWN) and (self.lane == GD.T_V_) ):
    #                         print('-------------------------              ---------------------------------')
    #                         #if(self.y < GD.rotate_point[self.direction][self.lane]):
    #                         self.y += self.speed
    def turn(self, coordinate : str , coordinate_sign : int , oposit_cordinate_sign : int, x_steps : int ,y_steps : int ,angel_sign : int, is_not_the_point_to_turn : bool, is_the_environment_allows_to_move_on : bool , the_rotation_has_end : bool)->bool:
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
                        # if(coordinate == 'x'):
                        #     self.y += self.speed*oposit_cordinate_sign
                        # elif(coordinate == 'y'):
                        #     self.x += self.speed*oposit_cordinate_sign
                        self.direction = GD.DOWN
                        if(self.lane == GD.CD):
                            self.lane = GD.D_F_
                        elif(self.lane == GD.KL):
                            self.lane = GD.L_N_
                        elif(self.lane == GD.ST):
                            self.lane = GD.T_V_
                        #print('ooooooooo')
                        if( (self.direction == GD.DOWN) and (self.lane == GD.T_V_) ):
                            print('-------------------------              ---------------------------------')
                            #if(self.y < GD.rotate_point[self.direction][self.lane]):
                            self.y += self.speed

#############################################################################################################################


    # def handle_turned_equal_zero(self, angel_sign:int, x_steps:int, y_steps:int):
    #     self.rotate_angle += GD.rotation_angle
    #     self.current_image = pygame.transform.rotate(self.original_image, angel_sign * self.rotate_angle)
    #     self.x += x_steps
    #     self.y += y_steps
    #     if (self.rotate_angle == 90):
    #         self.turned = 1


#############################################################################################################################
    
    
    # def applyMoving(self, coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right, y_steps_right, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right, coordinate_sign_left, oposit_cordinate_sign_left, x_steps_left, y_steps_left, is_not_the_point_to_turn_left, is_the_environment_allows_to_move_on_left, the_rotation_has_end_left, image_has_crossed_stop_line_now, it_can_move_straight):
    #     if(image_has_crossed_stop_line_now):
    #         self.crossed = 1
    #         #GD.vehicles_[self.direction]['crossed'] += 1
            
    #         # x
    #         if(self.lane == GD.IJ and self.x >= GD.points['K']['x']):
    #             #del GD.vehicles_[self.direction][self.lane][0]
    #             self.lane = GD.KL
    #           #  GD.vehicles_[self.direction][self.lane].append[self]
    #             self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

    #         elif(self.lane == GD.QR and self.x >= GD.points['S']['x']):
    #             #del GD.vehicles_[self.direction][self.lane][0]
    #             self.lane = GD.ST
    #             #GD.vehicles_[self.direction][self.lane].append[self]
    #             self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

    #         elif(self.lane == GD.HG and self.x <= GD.points['F']['x']):
    #            # del GD.vehicles_[self.direction][self.lane][0]
    #             self.lane = GD.FE
    #             #GD.vehicles_[self.direction][self.lane].append[self]
    #             len(GD.vehicles_[self.direction][self.lane]) - 1
    #             self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

    #         elif(self.lane == GD.PO and self.x <= GD.points['N']['x']):
    #             #del GD.vehicles_[self.direction][self.lane][0]
    #             self.lane = GD.NM
    #            # GD.vehicles_[self.direction][self.lane].append[self]
    #             len(GD.vehicles_[self.direction][self.lane]) - 1
    #             self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

    #         # y
    #         elif(self.lane == GD.D_F_ and self.y >= GD.points['J_']['y']):
    #             #del GD.vehicles_[self.direction][self.lane][0]
    #             self.lane = GD.J_Q_
    #            # GD.vehicles_[self.direction][self.lane].append[self]
    #             len(GD.vehicles_[self.direction][self.lane]) - 1
    #             self.index=len(GD.vehicles_[self.direction][self.lane]) - 1


    #         elif(self.lane == GD.L_N_ and self.y >= GD.points['R_']['y']):
    #             #del GD.vehicles_[self.direction][self.lane][0]
    #             self.lane = GD.R_W_
    #             #GD.vehicles_[self.direction][self.lane].append[self]
    #             len(GD.vehicles_[self.direction][self.lane]) - 1
    #             self.index=len(GD.vehicles_[self.direction][self.lane]) - 1


    #         elif(self.lane == GD.M_K_ and self.y <= GD.points['G_']['y']):
    #             #del GD.vehicles_[self.direction][self.lane][0]
    #             self.lane = GD.G_B_
    #             #GD.vehicles_[self.direction][self.lane].append[self]
    #             len(GD.vehicles_[self.direction][self.lane]) - 1
    #             self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

    #         elif(self.lane == GD.U_S_ and self.y <= GD.points['O_']['y']):
    #             #del GD.vehicles_[self.direction][self.lane][0]
    #             self.lane = GD.O_H_
    #             #GD.vehicles_[self.direction][self.lane].append[self]
    #             len(GD.vehicles_[self.direction][self.lane]) - 1
    #             self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

    def applyMoving(self, coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right, y_steps_right, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right, coordinate_sign_left, oposit_cordinate_sign_left, x_steps_left, y_steps_left, is_not_the_point_to_turn_left, is_the_environment_allows_to_move_on_left, the_rotation_has_end_left, image_has_crossed_stop_line_now, it_can_move_straight):
        if(image_has_crossed_stop_line_now):
            self.crossed = 1
            GD.vehicles_[self.direction]['crossed'] += 1
            # x
            if(self.lane == GD.IJ and self.x >= GD.points['K']['x']):
                #del GD.vehicles_[self.direction][self.lane][0]
                GD.vehicles_[self.direction][self.lane].pop(0)
                self.lane = GD.KL
                GD.vehicles_[self.direction][self.lane].append(self)
                self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

            elif(self.lane == GD.QR and self.x >= GD.points['S']['x']):
                GD.vehicles_[self.direction][self.lane].pop(0)
                self.lane = GD.ST
                GD.vehicles_[self.direction][self.lane].append(self)
                self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

            elif(self.lane == GD.HG and self.x <= GD.points['F']['x']):
                GD.vehicles_[self.direction][self.lane].pop(0)
                self.lane = GD.FE
                GD.vehicles_[self.direction][self.lane].append(self)
                self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

            elif(self.lane == GD.PO and self.x <= GD.points['N']['x']):
                GD.vehicles_[self.direction][self.lane].pop(0)
                self.lane = GD.NM
                GD.vehicles_[self.direction][self.lane].append(self)
                self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

            # y
            elif(self.lane == GD.D_F_ and self.y >= GD.points['J_']['y']):
                GD.vehicles_[self.direction][self.lane].pop(0)
                self.lane = GD.J_Q_
                GD.vehicles_[self.direction][self.lane].append(self)
                self.index=len(GD.vehicles_[self.direction][self.lane]) - 1


            elif(self.lane == GD.L_N_ and self.y >= GD.points['R_']['y']):
                GD.vehicles_[self.direction][self.lane].pop(0)
                self.lane = GD.R_W_
                GD.vehicles_[self.direction][self.lane].append(self)
                self.index=len(GD.vehicles_[self.direction][self.lane]) - 1


            elif(self.lane == GD.M_K_ and self.y <= GD.points['G_']['y']):
                GD.vehicles_[self.direction][self.lane].pop(0)
                self.lane = GD.G_B_
                GD.vehicles_[self.direction][self.lane].append(self)
                self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

            elif(self.lane == GD.U_S_ and self.y <= GD.points['O_']['y']):
                GD.vehicles_[self.direction][self.lane].pop(0)
                self.lane = GD.O_H_
                GD.vehicles_[self.direction][self.lane].append(self)
                self.index=len(GD.vehicles_[self.direction][self.lane]) - 1

    #      ##### Turned right #####
    #     if(self.will_turn_right == 1):
    #         self.turn( coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right ,y_steps_right,-1, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right)
    #         if( (self.direction == GD.DOWN) and (self.lane == GD.T_V_) ):
    #                 print('-------------------------              ---------------------------------')
    #                 #if(self.y < GD.rotate_point[self.direction][self.lane]):
    #                 self.y += self.speed*coordinate_sign_right
    #                 # else:
    #                 #     if(self.turn( 'y', coordinate_sign_right, -1, x_steps_right ,y_steps_right,-1, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right)):
    #                 #         self.direction = GD.LEFT
    #                 #         self.lsne = GD.VU
    #     ##### Turned left #####
    #     elif(self.will_turn_left == 1):
    #         self.turn( coordinate, coordinate_sign_left, oposit_cordinate_sign_left, x_steps_left ,y_steps_left,1, is_not_the_point_to_turn_left, is_the_environment_allows_to_move_on_left, the_rotation_has_end_left)
    #     else:
    #         if(it_can_move_straight):
    #             # if(coordinate == 'x'):
    #             #     self.x += self.speed*coordinate_sign_right
                    
    #             # elif(coordinate == 'y'):
    #             #     self.y += self.speed*coordinate_sign_right
    #             if(self.direction == GD.RIGHT and self.lane in [ GD.CD , GD.KL ,GD.ST]):
    #                 if(self.x < GD.rotate_point[self.direction][self.lane]):
    #                     self.x += self.speed*coordinate_sign_right
    #                 else:
    #                     if(self.turn( coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right ,y_steps_right,-1, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right)):
    #                         # self.direction = GD.DOWN
    #                         # if(self.lane == GD.CD):
    #                         #     self.lane = GD.D_F_
    #                         # elif(self.lane == GD.KL):
    #                         #     self.lane = GD.L_N_
    #                         # elif(self.lane == GD.ST):
    #                         #     self.lane = GD.T_V_
    #                         print('-------------------------iiiiiii---------------------------------')
                        
    #             # elif(self.lane in [ GD.BA , GD.KL ,GD.ST]):
    #             #     if(self.x < GD.rotate_point[self.direction][self.lane]):
    #             #         self.x += self.speed*coordinate_sign_right
    #             #     else:
    #             #         self.turn( coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right ,y_steps_right,-1, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right)
                            
    #             print(f"self.direction = {self.direction}    self.lane = {self.lane}       {self.direction == GD.DOWN and self.lane == GD.T_V_ }")
    #             print(f"x = {self.x}  y = {self.y}")
    #             if( (self.direction == GD.DOWN) and (self.lane == GD.T_V_) ):
    #                 print('-------------------------              ---------------------------------')
    #                 #if(self.y < GD.rotate_point[self.direction][self.lane]):
    #                 self.y += self.speed*coordinate_sign_right
    #                 # else:
    #                 #     if(self.turn( 'y', coordinate_sign_right, -1, x_steps_right ,y_steps_right,-1, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right)):
    #                 #         self.direction = GD.LEFT
    #                 #         self.lsne = GD.VU
    #         print('-------------------------ddddddddddd---------------------------------')
        
                    

#############################################################################################################################

    def move_(self):
        #print(GD.intersections[0].current_green)
        # RIGHT
        if(GD.cars_number>0):
            return
        if(self.direction == GD.RIGHT):
            # For Left Rotation
            x_steps_left =GD.steps_turning_vehicle[self.vehicle_class][self.direction]['left'][0]
            y_steps_left = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['left'][1]
            # For Right Rotation
            x_steps_right = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['right'][0]
            y_steps_right = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['right'][1]

            current_position   = self.x + 5#self.current_image.get_rect().width
            
            if(self.lane in [ GD.CD , GD.KL , GD.ST , GD.WX ]):
                #print(f"self.lane = {self.lane}  direction = {self.direction}  {GD.rotate_point[self.direction][self.lane]}")
                rotation_point     = GD.rotate_point[self.direction][self.lane]
                rotation_available = current_position >= rotation_point
    
                if(rotation_available):
                    self.rotate_angle += GD.rotation_angle
                    if(self.lane!=GD.WX):
                        self.x += x_steps_right
                        self.y -= y_steps_right
                    else:
                        self.x += x_steps_left
                        self.y -= y_steps_left

                    if(self.lane == GD.WX):
                        self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)
                    else:
                        self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)

                    if (self.rotate_angle == 90):#rotation finished
                        
                        next_direction = GD.next_lane_of[self.direction][self.lane][0]
                        next_lane      = GD.next_lane_of[self.direction][self.lane][1]
                       

             ##############################################################
                        GD.vehicles_[self.direction][self.lane].pop(0)
                        #GD.lanes_quantity[self.direction][self.lane] = GD.lanes_quantity[self.direction][self.lane]
                        #-self.current_image.get_rect().width-GD.gap
                        #GD.vehicles_[self.direction][self.lane].pop(0)
                          #  for vehicle in GD.vehicles_[self.direction][self.lane]:
                           #     vehicle.index = vehicle.index-1
                        self.direction = next_direction
                        self.lane      = next_lane
                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane

                       # if(len(GD.vehicles_[self.direction][self.lane])>=2):
                        #    if(self.speed< GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) + 1].speed):
                         #       self.speed=GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) + 1].speed
                        #self.index=len(GD.vehicles_[self.direction][self.lane]) - 1
             #########################################################################3
                        self.rotate_angle = 0
                        self.original_image = self.current_image
                 
                else:
                  #if(self.lane==GD.IJ && )
                    if(self in GD.vehicles_[self.direction][self.lane]):
                        if(len(GD.vehicles_[self.direction][self.lane])==1): # if there's no other cars
                            self.x = self.x + self.speed
                            #check if it's the first car so it can move freely , OR it won't pass the next car so it can also move
                        elif(( GD.vehicles_[self.direction][self.lane].index(self) == 0) or self.x + self.current_image.get_rect().width+GD.gap+self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                            self.x = self.x + self.speed
                            #check if we can move by replacing the speed with the next car's speed
                        elif(self.x + self.current_image.get_rect().width+GD.gap+GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                            self.x= self.x +GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                    else:
                        print(self.direction)
                        print(self.lane)
                        print("**************************************")
                        
                    
                
            # free choise weather to turn right/left or to keep streight
            elif(self.lane in [ GD.IJ , GD.QR ]):
                 #self.x = self.x + self.speed
                    #print(f" lane  =  {self.lane}")
                    if(self.lane == GD.IJ):
                        image_has_crossed_stop_line_now =  current_position >= GD.streets[self.direction][GD.KL]['x'][1] #GD.stop_lines[self.direction])
                    if(self.lane == GD.QR):
                        image_has_crossed_stop_line_now =  current_position >= GD.streets[self.direction][GD.ST]['x'][1] #GD.stop_lines[self.direction])    
                    if(image_has_crossed_stop_line_now):
                        GD.vehicles_[self.direction][self.lane].pop(0)

                        #GD.vehicles_[self.direction][self.lane].pop(0)
                        #for vehicle in GD.vehicles_[self.direction][self.lane]:
                         #   vehicle.index = vehicle.index-1
                       

                        #self.index=len(GD.vehicles_[self.direction][self.lane]) - 1
                        self.crossed = 1
                        if self.lane == GD.IJ:
                            GD.crossed[GD.FGKJ][self.direction]['crossed'] += 1
                        else:
                            GD.crossed[GD.NOSR][self.direction]['crossed'] += 1
                            
                        if(self.lane == GD.IJ ):
                            self.lane = GD.KL
                        elif(self.lane == GD.QR ):
                            self.lane = GD.ST
                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                    
                    #if(self.lane==GD.IJ && )
                    elif(self in GD.vehicles_[self.direction][self.lane]):
                        if(len(GD.vehicles_[self.direction][self.lane])==1):
                            self.x = self.x + self.speed
                            #add green color check 
                        elif(( GD.vehicles_[self.direction][self.lane].index(self) == 0) or self.x + self.current_image.get_rect().width+GD.gap+self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                            self.x = self.x + self.speed
                        elif(self.x + self.current_image.get_rect().width+GD.gap+GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                            self.x= self.x +GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                    else:
                        print(self.direction)
                        print(self.lane)
                        print("**************************************")
                            
                    
                   
                       # if(len(GD.vehicles_[self.direction][self.lane])>=2):
                        #    if(self.speed< GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) + 1].speed):
                         #       self.speed=GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) + 1].speed

                        
                      








        # DOWN                    
        if(self.direction == GD.DOWN):
            #self.y += self.speed
            # For Left Rotation
            x_steps_left =GD.steps_turning_vehicle[self.vehicle_class][self.direction]['left'][0]
            y_steps_left = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['left'][1]
            # For Right Rotation
            x_steps_right = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['right'][0]
            y_steps_right = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['right'][1]

            current_position   = self.y + self.current_image.get_rect().height -15
            
            if(self.lane in [ GD.A_I_ , GD.J_Q_ , GD.R_W_ , GD.T_V_ ]):
                #print(f"self.lane = {self.lane}  direction = {self.direction}  {GD.rotate_point[self.direction][self.lane]}")
                rotation_point     = GD.rotate_point[self.direction][self.lane]
                rotation_available = current_position >= rotation_point
    
                if(rotation_available):
                    self.rotate_angle += GD.rotation_angle
                    if(self.lane == GD.T_V_):
                        self.x -= x_steps_right
                        self.y += y_steps_right
                    else:
                        self.x-=x_steps_left
                        self.y +=y_steps_left
                    #self.y -= y_steps_right

                    
                    if(self.lane != GD.T_V_):
                        self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)
                    else:
                        self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)

                    if (self.rotate_angle == 90):
                          
                        next_direction = GD.next_lane_of[self.direction][self.lane][0]
                        next_lane      = GD.next_lane_of[self.direction][self.lane][1]
                        
                        GD.vehicles_[self.direction][self.lane].pop(0)

                        #    GD.vehicles_[self.direction][self.lane].pop(0)
                           # for vehicle in GD.vehicles_[self.direction][self.lane]:
                            #    vehicle.index = vehicle.index-1
                        self.direction = next_direction
                        self.lane      = next_lane
                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane

                       # self.index=len(GD.vehicles_[self.direction][self.lane]) - 1
                        self.rotate_angle = 0
                        self.original_image = self.current_image
                 
                else:
                    if(self in GD.vehicles_[self.direction][self.lane]):   
                        if(len(GD.vehicles_[self.direction][self.lane])==1):
                            self.y = self.y + self.speed
                            #check it can move forward    
                        elif(( GD.vehicles_[self.direction][self.lane].index(self) == 0) or self.y + self.current_image.get_rect().height +GD.gap+self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y):
                            self.y = self.y + self.speed
                        #increase the speed based on the next car speed if it's 
                        elif(self.y + self.current_image.get_rect().height +GD.gap+GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y):
                            self.y = self.y + GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                    else:
                        print(self.direction)
                        print(self.lane)
                        print("**************************************")
                    
                
            # free choise weather to turn right/left or to keep streight
            elif(self.lane in [ GD.D_F_ , GD.L_N_ ]):
                
                    #print(f" lane  =  {self.lane}")
                    if(self.lane == GD.D_F_):
                        image_has_crossed_stop_line_now =  current_position >= GD.streets[self.direction][GD.J_Q_]['y'][1] #GD.stop_lines[self.direction])
                    if(self.lane == GD.L_N_):
                        image_has_crossed_stop_line_now =  current_position >= GD.streets[self.direction][GD.R_W_]['y'][1] #GD.stop_lines[self.direction])    
                    if(image_has_crossed_stop_line_now):
                        #GD.vehicles_[self.direction][self.lane].pop(0)
                        #for vehicle in GD.vehicles_[self.direction][self.lane]:
                         #   vehicle.index = vehicle.index-1
                        GD.vehicles_[self.direction][self.lane].pop(0)

                    
                        #GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                        #self.index=len(GD.vehicles_[self.direction][self.lane]) - 1
                        self.crossed = 1

                        if self.lane == GD.D_F_:
                            GD.crossed[GD.FGKJ][self.direction]['crossed'] += 1
                        else:
                            GD.crossed[GD.NOSR][self.direction]['crossed'] += 1
                        #self.y = self.y + 5*self.speed  
                            
                        if(self.lane == GD.D_F_ ):
                            self.lane = GD.J_Q_
                        elif(self.lane == GD.L_N_ ):
                            self.lane = GD.R_W_
                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                    elif(self in GD.vehicles_[self.direction][self.lane]):   
                        if(len(GD.vehicles_[self.direction][self.lane])==1):
                            self.y = self.y + self.speed   
                        elif(( GD.vehicles_[self.direction][self.lane].index(self) == 0) or self.y + self.current_image.get_rect().height +GD.gap+self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y):
                            self.y = self.y + self.speed
                        elif(self.y + self.current_image.get_rect().height +GD.gap+GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y):
                            self.y = self.y + GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                    else:
                        print(self.direction)
                        print(self.lane)
                        print("**************************************")



        # LEFT   
        if(self.direction == GD.LEFT):
             # For Left Rotation
            x_steps_left =GD.steps_turning_vehicle[self.vehicle_class][self.direction]['left'][0]
            y_steps_left = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['left'][1]
            # For Right Rotation
            x_steps_right = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['right'][0]
            y_steps_right = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['right'][1]

            current_position   = self.x #self.current_image.get_rect().width
            
            if(self.lane in [ GD.BA , GD.FE , GD.NM , GD.VU ]):
                #print(f"self.lane = {self.lane}  direction = {self.direction}  {GD.rotate_point[self.direction][self.lane]}")
                rotation_point     = GD.rotate_point[self.direction][self.lane]
                rotation_available = current_position <= rotation_point
    
                if(rotation_available):
                    self.rotate_angle += GD.rotation_angle
                    if(self.lane != GD.BA):
                        self.x -= x_steps_right
                        self.y += y_steps_right
                    else:
                        self.x -= x_steps_left
                        self.y += y_steps_left

                    if(self.lane == GD.BA):
                        self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)
                    else:
                        self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)

                    if (self.rotate_angle == 90):
                        
                        next_direction = GD.next_lane_of[self.direction][self.lane][0]
                        next_lane      = GD.next_lane_of[self.direction][self.lane][1]
                        
                        GD.vehicles_[self.direction][self.lane].pop(0)

                        #GD.vehicles_[self.direction][self.lane].pop(0)
                        #for vehicle in GD.vehicles_[self.direction][self.lane]:
                        #   vehicle.index = vehicle.index-1
                        self.direction = next_direction
                        self.lane      = next_lane
                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane

                        #GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                        #self.index=len(GD.vehicles_[self.direction][self.lane]) - 1
                        self.rotate_angle = 0
                        self.original_image = self.current_image
                 
                else:
                    if(self in GD.vehicles_[self.direction][self.lane]):
                        if(len(GD.vehicles_[self.direction][self.lane])==1):
                            self.x = self.x - self.speed
                        elif(( GD.vehicles_[self.direction][self.lane].index(self) == 0) or self.x - self.current_image.get_rect().width-GD.gap-self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x):
                            self.x = self.x - self.speed
                        elif(self.x - self.current_image.get_rect().width-GD.gap-GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x):
                            self.x= self.x - GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                    else:
                        print(self.direction)
                        print(self.lane)
                        print("**************************************")
                    
                
            # free choise weather to turn right/left or to keep streight
            elif(self.lane in [ GD.PO , GD.HG ]):
                    #print(f" lane  =  {self.lane}")
                    if(self.lane == GD.PO):
                        image_has_crossed_stop_line_now =  current_position <= GD.streets[self.direction][GD.NM]['x'][1] #GD.stop_lines[self.direction])
                    if(self.lane == GD.HG):
                        image_has_crossed_stop_line_now =  current_position <= GD.streets[self.direction][GD.FE]['x'][1] #GD.stop_lines[self.direction])    
                    if(image_has_crossed_stop_line_now):
                        #GD.vehicles_[self.direction][self.lane].pop(0)
                        #for vehicle in GD.vehicles_[self.direction][self.lane]:
                         #   vehicle.index = vehicle.index-1
                        GD.vehicles_[self.direction][self.lane].pop(0)

                 
                        #GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                        #self.index=len(GD.vehicles_[self.direction][self.lane]) - 1
                        self.crossed = 1
                        # WE MUST ADD THE LANE ALSO AS PARAM
                        
                        if self.lane == GD.HG:
                            GD.crossed[GD.FGKJ][self.direction]['crossed'] += 1
                        else:
                            GD.crossed[GD.NOSR][self.direction]['crossed'] += 1
                            
                        if(self.lane == GD.PO ):
                            self.lane = GD.NM
                        elif(self.lane == GD.HG ):
                            self.lane = GD.FE

                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                    elif(self in GD.vehicles_[self.direction][self.lane]):
                        if(len(GD.vehicles_[self.direction][self.lane])==1):
                            self.x = self.x - self.speed
                        elif(( GD.vehicles_[self.direction][self.lane].index(self) == 0) or self.x - self.current_image.get_rect().width-GD.gap-self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x):
                            self.x = self.x - self.speed
                        elif(self.x - self.current_image.get_rect().width-GD.gap-GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x):
                            self.x= self.x - GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                    else:
                        print(self.direction)
                        print(self.lane)
                        print("**************************************")

                       







        # UP   
        if(self.direction == GD.UP):
            # For Left Rotation
            x_steps_left =GD.steps_turning_vehicle[self.vehicle_class][self.direction]['left'][0]
            y_steps_left = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['left'][1]
            # For Right Rotation
            x_steps_right = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['right'][0]
            y_steps_right = GD.steps_turning_vehicle[self.vehicle_class][self.direction]['right'][1]

            current_position   = self.y + self.current_image.get_rect().height -15
            
            if(self.lane in [ GD.E_C_ , GD.G_B_ , GD.O_H_ , GD.X_P_]):
                #print(f"self.lane = {self.lane}  direction = {self.direction}  {GD.rotate_point[self.direction][self.lane]}")
                rotation_point     = GD.rotate_point[self.direction][self.lane]
                rotation_available = current_position <= rotation_point
    
                if(rotation_available):
                    self.rotate_angle += GD.rotation_angle
                    if(self.lane== GD.E_C_):
                        self.x -= x_steps_right
                        self.y += y_steps_right
                    else:
                        self.x -= x_steps_left
                        self.y += y_steps_left
                    
                    if(self.lane != GD.E_C_):
                        self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)
                    else:
                        self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)

                    if (self.rotate_angle == 90):
                        
                        next_direction = GD.next_lane_of[self.direction][self.lane][0]
                        next_lane      = GD.next_lane_of[self.direction][self.lane][1]
                        #if(len(GD.vehicles_[self.direction][self.lane])>0):
                         #   GD.vehicles_[self.direction][self.lane].pop(0)
                          #  for vehicle in GD.vehicles_[self.direction][self.lane]:
                           #     vehicle.index = vehicle.index-1
                       
                        GD.vehicles_[self.direction][self.lane].pop(0)
   
                        self.direction = next_direction
                        self.lane      = next_lane
                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                        #GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                        #self.index=len(GD.vehicles_[self.direction][self.lane]) - 1
                        self.rotate_angle = 0
                        self.original_image = self.current_image
                 
                else:
                    if(self in GD.vehicles_[self.direction][self.lane]):
                        if(len(GD.vehicles_[self.direction][self.lane])==1):
                            self.y = self.y - self.speed
                        elif(( GD.vehicles_[self.direction][self.lane].index(self) == 0) 
                        or self.y - self.current_image.get_rect().height-GD.gap-self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y):                        
                            self.y = self.y - self.speed
                        elif(self.y - self.current_image.get_rect().height-GD.gap-GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y):                        
                            self.y = self.y - GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                    else:
                        print(self.direction)
                        print(self.lane)
                        print("**************************************")
                    
                
            # free choise weather to turn right/left or to keep streight
            elif(self.lane in [ GD.M_K_ , GD.U_S_ ]):
                    #print(f" lane  =  {self.lane}")
                        if(self.lane == GD.M_K_):
                            image_has_crossed_stop_line_now =  current_position <= GD.streets[self.direction][GD.G_B_]['y'][1] #GD.stop_lines[self.direction])
                        if(self.lane == GD.U_S_):
                            image_has_crossed_stop_line_now =  current_position <= GD.streets[self.direction][GD.O_H_]['y'][1] #GD.stop_lines[self.direction])    
                        if(image_has_crossed_stop_line_now):
                        #GD.vehicles_[self.direction][self.lane].pop(0)
                        #for vehicle in GD.vehicles_[self.direction][self.lane]:
                         #   vehicle.index = vehicle.index-1
                            GD.vehicles_[self.direction][self.lane].pop(0)

           
                        #GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                        #self.index=len(GD.vehicles_[self.direction][self.lane]) - 1
                            self.crossed = 1

                            if self.lane == GD.M_K_:
                                GD.crossed[GD.FGKJ][self.direction]['crossed'] += 1
                            else:
                                GD.crossed[GD.NOSR][self.direction]['crossed'] += 1
                            
                            if(self.lane == GD.M_K_ ):
                                self.lane = GD.G_B_
                            elif(self.lane == GD.U_S_ ):
                                self.lane = GD.O_H_
                            GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                        elif(self in GD.vehicles_[self.direction][self.lane]):
                            if(len(GD.vehicles_[self.direction][self.lane])==1):
                                self.y = self.y - self.speed
                            elif(( GD.vehicles_[self.direction][self.lane].index(self) == 0) 
                            or self.y - self.current_image.get_rect().height-GD.gap-self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y):                        
                                self.y = self.y - self.speed
                            elif(self.y - self.current_image.get_rect().height-GD.gap-GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y):                        
                                self.y = self.y - GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                        else:
                            print(self.direction)
                            print(self.lane)
                            print("**************************************")

                   


#############################################################################################################################



    def move(self):
        #####################################  RIGHT #####################################
       
        if(self.direction == GD.RIGHT):
            coordinate = 'x'
            
            coordinate_sign_right = 1
            oposit_cordinate_sign_right = 1
            x_steps_right = 1.5#2.2
            y_steps_right = 1#1.8
           
            is_not_the_point_to_turn_right = False
            if(self.lane in [ GD.IJ , GD.QR , GD.CD , GD.KL , GD.ST]):
                is_not_the_point_to_turn_right = (self.x + self.current_image.get_rect().width) < GD.rotate_point[self.direction][self.lane]
            
            
            
            is_the_environment_allows_to_move_on_right = True#(self.x + self.current_image.get_rect().width <= self.stop or (GD.current_green == 0 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.x + self.current_image.get_rect().width < (GD.vehicles[self.direction][self.lane][self.index - 1].x - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1)
            the_rotation_has_end_right = self.index == 0 or self.y+self.current_image.get_rect().height < (GD.vehicles_[self.direction][self.lane][self.index-1].y - GD.gap2) or self.x+self.current_image.get_rect().width < (GD.vehicles_[self.direction][self.lane][self.index-1].x - GD.gap2)
           
            coordinate_sign_left = 1
            oposit_cordinate_sign_left = -1
            x_steps_left = 2.2
            y_steps_left = -1.8
            
            #is_not_the_point_to_turn_left = (self.crossed == 0) or (self.x + self.current_image.get_rect().width < GD.mid[self.direction][self.lane][coordinate])
            is_not_the_point_to_turn_left = False
            if(self.lane in [ GD.IJ , GD.QR]):
                is_not_the_point_to_turn_left = (self.x + self.current_image.get_rect().width ) < GD.mid.get(self.direction)[self.lane]['x']


            is_the_environment_allows_to_move_on_left = True #(self.x + self.current_image.get_rect().width <= self.stop or (GD.current_green == 0 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.x + self.current_image.get_rect().width < (GD.vehicles_[self.direction][self.lane][self.index - 1].x - GD.gap2) or (GD.vehicles_[self.direction][self.lane][self.index - 1].turned == 1))
            the_rotation_has_end_left = (self.index == 0 )or (self.y+self.current_image.get_rect().height < (GD.vehicles_[self.direction][self.lane][self.index-1].x - GD.gap2)) or (self.x+self.current_image.get_rect().width < (GD.vehicles_[self.direction][self.lane][self.index-1].y - GD.gap2))
           
            image_has_crossed_stop_line_now = True#(self.crossed == 0 )and (self.x + self.current_image.get_rect().width > GD.stop_lines[self.direction])
            it_can_move_straight = True#((self.x+self.current_image.get_rect().width <= self.stop) or (self.crossed == 1 ) or (GD.current_green == 0 and GD.current_yellow == 0)) and ((self.index == 0) or (self.x + self.current_image.get_rect().width < (GD.vehicles_[self.direction][self.lane][self.index - 1].x - GD.gap2)) or ((GD.vehicles_[self.direction][self.lane][self.index - 1].turned == 1)))
           
        # #####################################  DOWN #####################################
        # elif(self.direction == GD.DOWN):
        #     coordinate = 'y'
            
        #     coordinate_sign_right = 1
        #     oposit_cordinate_sign_right = -1
        #     x_steps_right = -2.5
        #     y_steps_right = 2.2
        #     is_not_the_point_to_turn_right = (self.crossed == 0) or (self.y+self.current_image.get_rect().height < GD.directly[self.direction][coordinate])
        #     is_the_environment_allows_to_move_on_right = ((self.y + self.current_image.get_rect().height <= self.stop or (GD.current_green == 1 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.y + self.current_image.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index - 1].y - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
        #     the_rotation_has_end_right = (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.vehicles[self.direction][self.lane][self.index-1].current_image.get_rect().width + GD.gap2) or self.y < (GD.vehicles[self.direction][self.lane][self.index-1].y - GD.gap2))
           
        #     coordinate_sign_left = 1
        #     oposit_cordinate_sign_left = 1
        #     x_steps_left = 2.5
        #     y_steps_left = 2
        #     is_not_the_point_to_turn_left = (self.crossed == 0) or (self.y+self.current_image.get_rect().height  < GD.mid[self.direction][coordinate])
        #     is_the_environment_allows_to_move_on_left = ((self.y + self.current_image.get_rect().height <= self.stop or (GD.current_green == 1 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.y + self.current_image.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index - 1].y - GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
        #     the_rotation_has_end_left = (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].current_image.get_rect().width + GD.gap2) or self.y < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.gap2))
           
        #     image_has_crossed_stop_line_now = (self.crossed == 0 and self.y+self.current_image.get_rect().height > GD.stop_lines[self.direction])
        #     it_can_move_straight = ((self.y + self.current_image.get_rect().height <= self.stop or self.crossed == 1 or (GD.current_green == 1 and GD.current_yellow == 0)) and (self.index == 0 or self.y + self.current_image.get_rect().height < (GD.vehicles[self.direction][self.lane][self.index - 1].y - GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1)))
          
        # #####################################  LEFT #####################################
        # elif(self.direction == GD.LEFT):  
        #     coordinate = 'x'
            
        #     coordinate_sign_right = -1
        #     oposit_cordinate_sign_right = -1
        #     x_steps_right = -1.5
        #     y_steps_right = -2.5
        #     is_not_the_point_to_turn_right = (self.crossed == 0) or (self.x > GD.directly[self.direction][coordinate])
        #     is_the_environment_allows_to_move_on_right =((self.x >= self.stop or (GD.current_green == 2 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index - 1].x + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().width + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
        #     the_rotation_has_end_right = (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.vehicles[self.direction][self.lane][self.index-1].current_image.get_rect().width + GD.gap2) or self.x > (GD.vehicles[self.direction][self.lane][self.index-1].x + GD.gap2))
           
        #     coordinate_sign_left = -1
        #     oposit_cordinate_sign_left = 1
        #     x_steps_left = -1.8
        #     y_steps_left = 2.5
        #     is_not_the_point_to_turn_left = (self.crossed == 0) or (self.x > GD.mid[self.direction][coordinate])
        #     is_the_environment_allows_to_move_on_left = ((self.x >= self.stop or (GD.current_green == 2 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index - 1].x + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().width + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
        #     the_rotation_has_end_left = True
           
        #     image_has_crossed_stop_line_now = (self.crossed == 0 and self.x < GD.stop_lines[self.direction])
        #     it_can_move_straight = ((self.x >= self.stop or self.crossed == 1 or (GD.current_green == 2 and GD.current_yellow == 0)) and (self.index == 0 or self.x > (GD.vehicles[self.direction][self.lane][self.index - 1].x + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().width + GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1)))
          
        # #####################################  UP #####################################
        # elif(self.direction == GD.UP):   
        #     coordinate = 'y'
            
        #     coordinate_sign_right = -1
        #     oposit_cordinate_sign_right = 1
        #     x_steps_right = 1
        #     y_steps_right = -1
        #     is_not_the_point_to_turn_right = (self.crossed == 0) or (self.y > GD.directly[self.direction][coordinate])
        #     is_the_environment_allows_to_move_on_right =((self.y >= self.stop or (GD.current_green == 3 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index - 1].y + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().height + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
        #     the_rotation_has_end_right = (self.index == 0 or self.x < (GD.vehicles[self.direction][self.lane][self.index-1].x - GD.vehicles[self.direction][self.lane][self.index-1].current_image.get_rect().width - GD.gap2) or self.y > (GD.vehicles[self.direction][self.lane][self.index-1].y + GD.gap2))
           
        #     coordinate_sign_left = -1
        #     oposit_cordinate_sign_left = -1
        #     x_steps_left = -1.8
        #     y_steps_left = -2.5
        #     is_not_the_point_to_turn_left = (self.crossed == 0) or (self.y > GD.mid[self.direction][coordinate])
        #     is_the_environment_allows_to_move_on_left = ((self.y >= self.stop or (GD.current_green == 3 and GD.current_yellow == 0) or self.crossed == 1) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index - 1].y + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().height + GD.gap2) or GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1))
        #     the_rotation_has_end_left = True
           
        #     image_has_crossed_stop_line_now = (self.crossed == 0 and self.y < GD.stop_lines[self.direction])
        #     it_can_move_straight =((self.y >= self.stop or self.crossed == 1 or (GD.current_green == 3 and GD.current_yellow == 0)) and (self.index == 0 or self.y > (GD.vehicles[self.direction][self.lane][self.index - 1].y + GD.vehicles[self.direction][self.lane][self.index - 1].current_image.get_rect().height + GD.gap2) or (GD.vehicles[self.direction][self.lane][self.index - 1].turned == 1)))
        
            self.applyMoving(coordinate, coordinate_sign_right, oposit_cordinate_sign_right, x_steps_right, y_steps_right, is_not_the_point_to_turn_right, is_the_environment_allows_to_move_on_right, the_rotation_has_end_right, coordinate_sign_left,oposit_cordinate_sign_left, x_steps_left, y_steps_left, is_not_the_point_to_turn_left, is_the_environment_allows_to_move_on_left, the_rotation_has_end_left, image_has_crossed_stop_line_now, it_can_move_straight)











    # def get_direction_after_rotate(self , rotate_to : str) -> str:
    #     direction = self.direction
    #     new_direction = ''

    #     if direction == GD.RIGHT:
    #         if rotate_to == 'left':
    #             new_direction = GD.UP
    #         elif rotate_to == 'right':
    #             new_direction = GD.DOWN

    #     elif direction == GD.LEFT:
    #         if rotate_to == 'left':
    #             new_direction = GD.DOWN
    #         elif rotate_to == 'right':
    #             new_direction = GD.UP

    #     elif direction == GD.DOWN:
    #         if rotate_to == 'left':
    #             new_direction = GD.RIGHT
    #         elif rotate_to == 'right':
    #             new_direction = GD.LEFT

    #     elif direction == GD.UP:
    #         if rotate_to == 'left':
    #             new_direction = GD.LEFT
    #         elif rotate_to == 'right':
    #             new_direction = GD.RIGHT

    #     return new_direction

    
    # def get_oposite_direction(self,direction:str)->str:# no need
    #     if direction == GD.UP:
    #         return GD.DOWN
    #     if direction == GD.DOWN:
    #         return GD.UP
    #     if direction == GD.LEFT:
    #         return GD.RIGHT
    #     return GD.LEFT


    # weight of vehicle  = GD.vehiclesWeight[self.vehicleClass]

    # def get_lane_coordinate_after_rotation(self ,dir, coordinate ):# no need
    #     direction = dir
    #     print('{} == {} : {}'.format(self.direction , dir , self.direction == dir))
    #     print('x befor : {}'.format(self.x))
    #     if coordinate == 'x':
    #         if direction == GD.UP:
    #             self.x = GD.drive_orginizer[GD.DOWN]
    #         elif direction == GD.DOWN:
    #             self.x = GD.drive_orginizer[GD.UP]
    #         elif direction == GD.LEFT:
    #             self.x = GD.drive_orginizer[GD.RIGHT]
    #         elif direction == GD.RIGHT:
    #             self.x = GD.drive_orginizer[GD.LEFT]
    #     print('x after : {}'.format(self.x))
    #     if coordinate == 'y':
    #         if direction == GD.UP:
    #             self.y = GD.drive_orginizer[GD.DOWN]
    #         elif direction == GD.DOWN:
    #             self.y = GD.drive_orginizer[GD.UP]
    #         elif direction == GD.LEFT:
    #             self.y = GD.drive_orginizer[GD.RIGHT]
    #         elif direction == GD.RIGHT:
    #             self.y = GD.drive_orginizer[GD.LEFT]
