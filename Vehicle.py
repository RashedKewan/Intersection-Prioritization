import math
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
        self.original_image = pygame.image.load(path).convert_alpha()
        self.current_image = pygame.image.load(path).convert_alpha()
        
        #######
        self.image = self.current_image.get_rect()
        self.all_sprites = pygame.sprite.Group(self) 
        self.speed_avg = 0
        self.Kilometre = 0

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
        
    def apply_circle_rotation_helper(self):
            center = pygame.math.Vector2(GD.circle_coordinates[self.direction][self.lane]['pos']) + pygame.math.Vector2( GD.circle_params_for_rotation[self.direction][self.lane][0] *GD.circle_coordinates[self.direction][self.lane]['radius'], GD.circle_params_for_rotation[self.direction][self.lane][1] *GD.circle_coordinates[self.direction][self.lane]['radius'] ).rotate( GD.circle_params_for_rotation[self.direction][self.lane][2] *self.rotate_angle )
            self.image = pygame.transform.rotate(self.original_image, GD.circle_params_for_rotation[self.direction][self.lane][3]*self.rotate_angle)
            self.rect = self.image.get_rect(center = (round(center.x), round(center.y)))
            self.rotate_angle = (self.rotate_angle + 1.9) % 90
            self.x = self.rect.x
            self.y = self.rect.y

    def apply_circle_rotation(self,screen):
        if(self.rotate_angle < 88):
            self.apply_circle_rotation_helper()
            self.all_sprites.draw(screen)
            return True
        self.rotate_angle = 90
        return False


#############################################################################################################################

    def move_(self,screen):
        prev_x = self.x
        prev_y = self.y
        ### added
        rotate_prossece_on = False
        ### 
        # RIGHT
        if(GD.cars_number>0):
            return
        if(self.direction == GD.RIGHT):
            current_position   = self.x + 5#self.current_image.get_rect().width
            
            if(self.lane in [ GD.CD , GD.KL , GD.ST , GD.WX ]):
                rotation_point     = GD.rotate_point[self.direction][self.lane]
                rotation_available = current_position >= rotation_point
                next_direction     = GD.next_lane_of[self.direction][self.lane][0]
                next_lane          = GD.next_lane_of[self.direction][self.lane][1]
                
                max_vehicle_number_in_next_lane = 1
                if (self.lane in [ GD.ST , GD.CD ]):
                    max_vehicle_number_in_next_lane = 2
                elif (self.lane == GD.WX ):
                    max_vehicle_number_in_next_lane = 3
                
                if(rotation_available and ( GD.vehicles_[self.direction][self.lane].index(self) == 0) ):
                        if (len(GD.vehicles_[next_direction][next_lane]) > max_vehicle_number_in_next_lane  ):
                            if(self.lane != GD.WX):
                                if(self.rotate_angle > 40):
                                    vehicle_can_move_without_crash  = (self.y  < GD.vehicles_[self.direction][self.lane][len(GD.vehicles_[self.direction][self.lane])- 1].y) 
                                    if(vehicle_can_move_without_crash):
                                        rotate_prossece_on = self.apply_circle_rotation(screen)
                                    else:
                                        self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)
                                else:
                                    rotate_prossece_on = self.apply_circle_rotation(screen)
                                   
                            else:
                                if(self.rotate_angle > 40):
                                    vehicle_can_move_without_crash  = (self.y  > GD.vehicles_[self.direction][self.lane][len(GD.vehicles_[self.direction][self.lane])- 1].y) 
                                    if(vehicle_can_move_without_crash): 
                                        rotate_prossece_on = self.apply_circle_rotation(screen)
                                    else:
                                        self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)
                                else:
                                    rotate_prossece_on = self.apply_circle_rotation(screen)
                                   
                        else:
                            rotate_prossece_on = self.apply_circle_rotation(screen)
                           
                        if (self.rotate_angle == 90):#rotation finished
                            if(self.lane == GD.WX):
                                self.current_image = pygame.transform.rotate(self.original_image, 1 * (self.rotate_angle))
                            else:
                                self.current_image = pygame.transform.rotate(self.original_image, -1 * (self.rotate_angle))




                            next_direction = GD.next_lane_of[self.direction][self.lane][0]
                            next_lane      = GD.next_lane_of[self.direction][self.lane][1]
                        
                            GD.vehicles_[self.direction][self.lane].pop(0)
                        
                            self.direction = next_direction
                            self.lane      = next_lane
                            GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane

                            self.rotate_angle = 0
                            self.original_image = self.current_image
                 
                else:
                    if(self in GD.vehicles_[self.direction][self.lane]):
                        if(len(GD.vehicles_[self.direction][self.lane])==1): # if there's no other cars
                            self.x = self.x + self.speed
                            #check if it's the first car so it can move freely , OR it won't pass the next car so it can also move
                        elif(( GD.vehicles_[self.direction][self.lane].index(self) == 0) or self.x + self.current_image.get_rect().width+GD.gap+self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                            self.x = self.x + self.speed
                            #check if we can move by replacing the speed with the next car's speed
                        elif(self.x + self.current_image.get_rect().width+GD.gap+GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                            self.x= self.x +GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                    
                
            # free choise weather to turn right/left or to keep streight
            elif(self.lane in [ GD.IJ , GD.QR ]):
                    next_direction     = GD.next_lane_of[self.direction][self.lane][0]
                    next_lane          = GD.next_lane_of[self.direction][self.lane][1]
                    intersection = GD.FGKJ 
                    if(self.lane == GD.QR ):
                        intersection = GD.NOSR
                    if(len(GD.vehicles_[next_direction][next_lane])<3):
                       
                        vehicle_is_first                = ( GD.vehicles_[self.direction][self.lane].index(self) == 0)
                        vehicle_didnt_reaches_stop_line = (self.x+self.current_image.get_rect().width <= GD.stop_lines[self.direction][intersection])
                        vehicle_crossed_intersection    = (self.crossed == 1 )
                        signal_not_red                  = (GD.intersections[intersection].current_green == 0 and GD.intersections[intersection].current_yellow == 0)
                        vehicle_can_move_without_crash  = (self.x + self.current_image.get_rect().width + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x) 
                        it_can_move_straight = ( 
                                                    vehicle_didnt_reaches_stop_line or 
                                                    vehicle_crossed_intersection    or 
                                                    signal_not_red                
                                                ) and (
                                                    #(self.index == 0)               or 
                                                    vehicle_can_move_without_crash         #((GD.vehicles_[self.direction][self.lane][self.index - 1].turned == 1)))
                                                )
                        #if( (GD.vehicles_[self.direction][self.lane]) > 1 )
                        #if red
                        if(not signal_not_red):
                            if(vehicle_didnt_reaches_stop_line ):
                                if(not vehicle_is_first and self.x + self.current_image.get_rect().width + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                                    self.x= self.x +GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                                elif(vehicle_is_first):
                                    self.x = self.x + self.speed
                        else:
                            if(it_can_move_straight):
                                self.x = self.x + self.speed

                            if( vehicle_is_first or self.x + self.current_image.get_rect().width + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                                self.x = self.x + self.speed
                            elif(self.x + self.current_image.get_rect().width + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                                self.x= self.x +GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                        


                        image_has_crossed_stop_line_now =  current_position >= GD.stop_lines[self.direction][GD.FGKJ]
                        if(self.lane == GD.QR):
                            image_has_crossed_stop_line_now =  current_position >= GD.stop_lines[self.direction][GD.NOSR]    
                        
                        if(image_has_crossed_stop_line_now):
                            GD.vehicles_[self.direction][self.lane].pop(0)
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
                    else:
                        vehicle_didnt_reaches_stop_line = (self.x+self.current_image.get_rect().width <= GD.stop_lines[self.direction][intersection])
                        vehicle_can_move_without_crash  = (self.x + self.current_image.get_rect().width + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x) 
                        vehicle_is_first                = ( GD.vehicles_[self.direction][self.lane].index(self) == 0)
                        if((vehicle_is_first and vehicle_didnt_reaches_stop_line) or (vehicle_didnt_reaches_stop_line and vehicle_can_move_without_crash)):
                            self.x= self.x + self.speed








        # DOWN                    
        if(self.direction == GD.DOWN):
            current_position   = self.y + self.current_image.get_rect().height -15
            
            if(self.lane in [ GD.A_I_ , GD.J_Q_ , GD.R_W_ , GD.T_V_ ]):
                rotation_point     = GD.rotate_point[self.direction][self.lane]
                rotation_available = current_position >= rotation_point
                next_direction = GD.next_lane_of[self.direction][self.lane][0]
                next_lane      = GD.next_lane_of[self.direction][self.lane][1]


                max_vehicle_number_in_next_lane = 1
                if (self.lane in [GD.R_W_] ):
                    max_vehicle_number_in_next_lane = 3
                elif (self.lane in [ GD.A_I_ , GD.J_Q_,GD.T_V_]):
                    max_vehicle_number_in_next_lane = 2
                
                if(rotation_available and ( GD.vehicles_[self.direction][self.lane].index(self) == 0) ):
                    if (len(GD.vehicles_[next_direction][next_lane]) > max_vehicle_number_in_next_lane ):
                        if(self.lane  == GD.T_V_):
                            if(self.rotate_angle > 40):
                                vehicle_can_move_without_crash  = (self.x  > GD.vehicles_[self.direction][self.lane][len(GD.vehicles_[self.direction][self.lane])- 1].x) 
                                if(vehicle_can_move_without_crash): 
                                    rotate_prossece_on = self.apply_circle_rotation(screen)
                                else:
                                    self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)
                            else:
                                rotate_prossece_on = self.apply_circle_rotation(screen)
                                
                        else:
                            if(self.rotate_angle > 40):
                                vehicle_can_move_without_crash  = (self.x  < GD.vehicles_[self.direction][self.lane][len(GD.vehicles_[self.direction][self.lane])- 1].x) 
                                if(vehicle_can_move_without_crash): 
                                    rotate_prossece_on = self.apply_circle_rotation(screen)
                                else:
                                        self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)
                            else:
                                rotate_prossece_on = self.apply_circle_rotation(screen)
                               

                    else:
                        rotate_prossece_on = self.apply_circle_rotation(screen)
                       
                    if (self.rotate_angle == 90):
                        if(self.lane != GD.T_V_):
                            self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)
                        else:
                            self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)

                        next_direction = GD.next_lane_of[self.direction][self.lane][0]
                        next_lane      = GD.next_lane_of[self.direction][self.lane][1]
                        GD.vehicles_[self.direction][self.lane].pop(0)
                        self.direction = next_direction
                        self.lane      = next_lane
                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
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
                    
                
            # free choise weather to turn right/left or to keep streight
            elif(self.lane in [ GD.D_F_ , GD.L_N_ ]):
                    next_direction     = GD.next_lane_of[self.direction][self.lane][0]
                    next_lane          = GD.next_lane_of[self.direction][self.lane][1]
                    intersection = GD.FGKJ 
                    if(self.lane == GD.L_N_ ):
                        intersection = GD.NOSR
                        
                    if(len(GD.vehicles_[next_direction][next_lane])<3):
                       
                        vehicle_is_first                = ( GD.vehicles_[self.direction][self.lane].index(self) == 0)
                        vehicle_didnt_reaches_stop_line = (self.y+self.current_image.get_rect().height <= GD.stop_lines[self.direction][intersection])
                        vehicle_crossed_intersection    = (self.crossed == 1 )
                        signal_not_red                  = (GD.intersections[intersection].current_green == 1 and GD.intersections[intersection].current_yellow == 0)
                        vehicle_can_move_without_crash  = (self.y + self.current_image.get_rect().height + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y) 
                        it_can_move_straight = ( 
                                                    vehicle_didnt_reaches_stop_line or 
                                                    vehicle_crossed_intersection    or 
                                                    signal_not_red                
                                                ) and (
                                                    #(self.index == 0)               or 
                                                    vehicle_can_move_without_crash         #((GD.vehicles_[self.direction][self.lane][self.index - 1].turned == 1)))
                                                )
                        #if red
                        if(not signal_not_red):
                            if(vehicle_didnt_reaches_stop_line ):
                                if(not vehicle_is_first and self.y + self.current_image.get_rect().height + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y ):
                                    self.y = self.y +GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                                elif(vehicle_is_first):
                                    self.y = self.y + self.speed
                        else:
                            if(it_can_move_straight):
                                self.y = self.y + self.speed

                            if( vehicle_is_first or self.y + self.current_image.get_rect().height + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y ):
                                self.y = self.y + self.speed
                            elif(self.y + self.current_image.get_rect().height + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y ):
                                self.y = self.y +GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                        
                        image_has_crossed_stop_line_now =  current_position >= GD.stop_lines[self.direction][GD.FGKJ]
                        if(self.lane == GD.L_N_):
                            image_has_crossed_stop_line_now =  current_position >= GD.stop_lines[self.direction][GD.NOSR]    
                        if(image_has_crossed_stop_line_now):
                            #GD.vehicles_[self.direction][self.lane].pop(0)
                            #for vehicle in GD.vehicles_[self.direction][self.lane]:
                            #   vehicle.index = vehicle.index-1
                            GD.vehicles_[self.direction][self.lane].pop(0)

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
                    else:
                        vehicle_didnt_reaches_stop_line = (self.y+self.current_image.get_rect().height <= GD.stop_lines[self.direction][intersection])
                        vehicle_can_move_without_crash  = (self.y + self.current_image.get_rect().height + GD.gap + self.speed < GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y) 
                        vehicle_is_first                = ( GD.vehicles_[self.direction][self.lane].index(self) == 0)
                        if((vehicle_is_first and vehicle_didnt_reaches_stop_line) or (vehicle_didnt_reaches_stop_line and vehicle_can_move_without_crash)):
                            self.y= self.y + self.speed

        # LEFT   
        if(self.direction == GD.LEFT):
            current_position   = self.x #self.current_image.get_rect().width

            if(self.lane in [ GD.BA , GD.FE , GD.NM , GD.VU ]):
                rotation_point     = GD.rotate_point[self.direction][self.lane]
                rotation_available = current_position <= rotation_point
                next_direction     = GD.next_lane_of[self.direction][self.lane][0]
                next_lane          = GD.next_lane_of[self.direction][self.lane][1]

                max_vehicle_number_in_next_lane = 1
                if (self.lane in [GD.FE ,GD.VU] ):
                    max_vehicle_number_in_next_lane = 2
                elif (self.lane in [GD.BA ] ):
                    max_vehicle_number_in_next_lane = 3
                
                if(rotation_available and ( GD.vehicles_[self.direction][self.lane].index(self) == 0) ):
                    if (len(GD.vehicles_[next_direction][next_lane]) > max_vehicle_number_in_next_lane ):
                        if(self.lane != GD.BA):
                            if(self.rotate_angle > 40):
                                vehicle_can_move_without_crash  = (self.y  > GD.vehicles_[self.direction][self.lane][len(GD.vehicles_[self.direction][self.lane])- 1].y) 
                                if(vehicle_can_move_without_crash):
                                    rotate_prossece_on = self.apply_circle_rotation(screen)
                                else:
                                    self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)   
                            else:
                                rotate_prossece_on = self.apply_circle_rotation(screen)
                                
                        else:
                            if(self.rotate_angle > 40):
                                vehicle_can_move_without_crash  = (self.y  < GD.vehicles_[self.direction][self.lane][len(GD.vehicles_[self.direction][self.lane])- 1].y) 
                                if(vehicle_can_move_without_crash):
                                    rotate_prossece_on = self.apply_circle_rotation(screen)
                                else:
                                    self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)   
                            else:
                                rotate_prossece_on = self.apply_circle_rotation(screen)
        
                    else:
                        rotate_prossece_on = self.apply_circle_rotation(screen)

                    if (self.rotate_angle == 90):
                        if(self.lane == GD.BA):
                            self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)
                        else:
                            self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)
                       
                        next_direction = GD.next_lane_of[self.direction][self.lane][0]
                        next_lane      = GD.next_lane_of[self.direction][self.lane][1]
                        
                        GD.vehicles_[self.direction][self.lane].pop(0)
                        self.direction = next_direction
                        self.lane      = next_lane
                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
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
                    
                    
                
            # free choise weather to turn right/left or to keep streight
            elif(self.lane in [ GD.PO , GD.HG ]):
                next_direction     = GD.next_lane_of[self.direction][self.lane][0]
                next_lane          = GD.next_lane_of[self.direction][self.lane][1]
                #  intersection
                intersection = GD.FGKJ 
                if(self.lane == GD.PO ):
                    intersection = GD.NOSR
                if(len(GD.vehicles_[next_direction][next_lane])<3):
                        #  intersection    
                    
                    
                    
                    # if(len(GD.vehicles_[self.direction][self.lane])==1):
                    #     self.x = self.x + self.speed
                    #         #add green color check 
                    vehicle_is_first                = ( GD.vehicles_[self.direction][self.lane].index(self) == 0)
                    vehicle_didnt_reaches_stop_line = (self.x-self.current_image.get_rect().width >= GD.stop_lines[self.direction][intersection])
                    vehicle_crossed_intersection    = (self.crossed == 1 )
                    signal_not_red                  = (GD.intersections[intersection].current_green == 2 and GD.intersections[intersection].current_yellow == 0)
                    vehicle_can_move_without_crash  = (self.x - self.current_image.get_rect().width - GD.gap - self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x) 
                    it_can_move_straight = ( 
                                                vehicle_didnt_reaches_stop_line or 
                                                vehicle_crossed_intersection    or 
                                                signal_not_red                
                                            ) and (
                                                #(self.index == 0)               or 
                                                vehicle_can_move_without_crash         #((GD.vehicles_[self.direction][self.lane][self.index - 1].turned == 1)))
                                            )
                    #if red
                    if(not signal_not_red):
                        if(vehicle_didnt_reaches_stop_line ):
                            if(not vehicle_is_first and ((self.x - self.current_image.get_rect().width - GD.gap - self.speed) > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x) ):
                                self.x= self.x - GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                            elif(vehicle_is_first):
                                self.x = self.x - self.speed
                    else:
                        if(it_can_move_straight):
                            self.x = self.x - self.speed

                        if( vehicle_is_first or self.x - self.current_image.get_rect().width - GD.gap - self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                            self.x = self.x - self.speed
                        elif(self.x - self.current_image.get_rect().width - GD.gap - self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x ):
                            self.x = self.x - GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                    
                    image_has_crossed_stop_line_now =  current_position <= GD.stop_lines[self.direction][GD.FGKJ]
                    if(self.lane == GD.PO):
                        image_has_crossed_stop_line_now =  current_position <= GD.stop_lines[self.direction][GD.NOSR]
                    
                    if(image_has_crossed_stop_line_now):
                        GD.vehicles_[self.direction][self.lane].pop(0)
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
                else:
                    vehicle_didnt_reaches_stop_line = (self.x-self.current_image.get_rect().width >= GD.stop_lines[self.direction][intersection])
                    vehicle_can_move_without_crash  = (self.x - self.current_image.get_rect().width - GD.gap - self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].x) 
                    vehicle_is_first                = ( GD.vehicles_[self.direction][self.lane].index(self) == 0)
                    if((vehicle_is_first and vehicle_didnt_reaches_stop_line) or (vehicle_didnt_reaches_stop_line and vehicle_can_move_without_crash)):
                        self.x= self.x - self.speed






        # UP   
        if(self.direction == GD.UP):
            current_position   = self.y + self.current_image.get_rect().height -15
            
            if(self.lane in [ GD.E_C_ , GD.G_B_ , GD.O_H_ , GD.X_P_]):
                rotation_point     = GD.rotate_point[self.direction][self.lane]
                rotation_available = current_position <= rotation_point
                next_direction     = GD.next_lane_of[self.direction][self.lane][0]
                next_lane          = GD.next_lane_of[self.direction][self.lane][1]

                max_vehicle_number_in_next_lane = 1
                if (self.lane in [GD.E_C_,GD.X_P_, GD.O_H_] ):
                    max_vehicle_number_in_next_lane = 2
                else:
                    max_vehicle_number_in_next_lane = 3
                
                if(rotation_available and ( GD.vehicles_[self.direction][self.lane].index(self) == 0) ):
                    # self.current_image = pygame.transform.rotate(self.original_image, 1 * 90)
                    # self.image = self.current_image.get_rect()
                    if (len(GD.vehicles_[next_direction][next_lane]) > max_vehicle_number_in_next_lane ):
                        if(self.lane == GD.E_C_):
                            if(self.rotate_angle > 40):
                                vehicle_can_move_without_crash  = (self.x  < GD.vehicles_[self.direction][self.lane][len(GD.vehicles_[self.direction][self.lane])- 1].x) 
                                if(vehicle_can_move_without_crash):
                                    rotate_prossece_on = self.apply_circle_rotation(screen) 
                                else:
                                    self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)
                            else:
                                rotate_prossece_on = self.apply_circle_rotation(screen)
                                
                        else:
                            if(self.rotate_angle > 40):
                                vehicle_can_move_without_crash  = (self.x  > GD.vehicles_[self.direction][self.lane][len(GD.vehicles_[self.direction][self.lane])- 1].x) 
                                if(vehicle_can_move_without_crash):
                                    rotate_prossece_on = self.apply_circle_rotation(screen) 
                                else:
                                    self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)    
                            else:
                                rotate_prossece_on = self.apply_circle_rotation(screen)
                                

                    else:
                        rotate_prossece_on = self.apply_circle_rotation(screen)
                        
                    if (self.rotate_angle == 90):
                        if(self.lane != GD.E_C_):
                            self.current_image = pygame.transform.rotate(self.original_image, 1 * self.rotate_angle)
                        else:
                            self.current_image = pygame.transform.rotate(self.original_image, -1 * self.rotate_angle)

                        next_direction = GD.next_lane_of[self.direction][self.lane][0]
                        next_lane      = GD.next_lane_of[self.direction][self.lane][1]
                    
                        GD.vehicles_[self.direction][self.lane].pop(0)
   
                        self.direction = next_direction
                        self.lane      = next_lane
                        GD.vehicles_[self.direction][self.lane].append(self) #add the car to the next lane
                       
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
                    
                    
                
            # free choise weather to turn right/left or to keep streight
            elif(self.lane in [ GD.M_K_ , GD.U_S_ ]):
                    next_direction     = GD.next_lane_of[self.direction][self.lane][0]
                    next_lane          = GD.next_lane_of[self.direction][self.lane][1]
                    intersection = GD.FGKJ 
                    if(self.lane == GD.U_S_ ):
                        intersection = GD.NOSR
                    if(len(GD.vehicles_[next_direction][next_lane])<3):
                        #  intersection
                        #  intersection
                        
                        
                        # if(len(GD.vehicles_[self.direction][self.lane])==1):
                        #     self.x = self.x + self.speed
                        #         #add green color check 
                        vehicle_is_first                = ( GD.vehicles_[self.direction][self.lane].index(self) == 0)
                        vehicle_didnt_reaches_stop_line = (self.y-self.current_image.get_rect().height >= GD.stop_lines[self.direction][intersection])
                        vehicle_crossed_intersection    = (self.crossed == 1 )
                        signal_not_red                  = (GD.intersections[intersection].current_green == 3 and GD.intersections[intersection].current_yellow == 0)
                        vehicle_can_move_without_crash  = (self.y - self.current_image.get_rect().height - GD.gap - self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y) 
                        it_can_move_straight = ( 
                                                    vehicle_didnt_reaches_stop_line or 
                                                    vehicle_crossed_intersection    or 
                                                    signal_not_red                
                                                ) and (
                                                    #(self.index == 0)               or 
                                                    vehicle_can_move_without_crash         #((GD.vehicles_[self.direction][self.lane][self.index - 1].turned == 1)))
                                                )
                        #if red
                        if(not signal_not_red):
                            if(vehicle_didnt_reaches_stop_line ):
                                if(not vehicle_is_first and ((self.y - self.current_image.get_rect().height - GD.gap - self.speed) > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y) ):
                                    self.y = self.y - GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                                elif(vehicle_is_first):
                                    self.y = self.y - self.speed
                        else:
                            if(it_can_move_straight):
                                self.y = self.y - self.speed

                            if( vehicle_is_first or self.y - self.current_image.get_rect().height - GD.gap - self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y ):
                                self.y = self.y - self.speed
                            elif(self.y - self.current_image.get_rect().height - GD.gap - self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y ):
                                self.y = self.y - GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].speed
                        
                        
                        image_has_crossed_stop_line_now =  current_position <= GD.stop_lines[self.direction][GD.FGKJ]
                        if(self.lane == GD.U_S_):
                            image_has_crossed_stop_line_now =  current_position <= GD.stop_lines[self.direction][GD.NOSR]
                        
                        if(image_has_crossed_stop_line_now):
                            GD.vehicles_[self.direction][self.lane].pop(0)
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
                    else:
                        vehicle_didnt_reaches_stop_line = (self.y-self.current_image.get_rect().height >= GD.stop_lines[self.direction][intersection])
                        vehicle_can_move_without_crash  = (self.y - self.current_image.get_rect().height - GD.gap - self.speed > GD.vehicles_[self.direction][self.lane][GD.vehicles_[self.direction][self.lane].index(self) - 1].y) 
                        vehicle_is_first                = ( GD.vehicles_[self.direction][self.lane].index(self) == 0)
                        if((vehicle_is_first and vehicle_didnt_reaches_stop_line) or (vehicle_didnt_reaches_stop_line and vehicle_can_move_without_crash)):
                            self.y= self.y - self.speed


        self.crossed = 0
        # Increase Kilometres
        if(prev_x != self.x and prev_y == self.y):
            self.Kilometre += abs(self.x - prev_x)
        elif(prev_x == self.x and prev_y != self.y):
            self.Kilometre += abs(self.y - prev_y)
        else:
            x = self.x - prev_x
            y = self.y - prev_y
            self.Kilometre += math.sqrt( x*x + y*y )

        #Calculate speed_avg
        self.speed_avg = self.Kilometre / GD.time_elapsed
        
        if(rotate_prossece_on == False):
            screen.blit(self.current_image, [self.x, self.y])
