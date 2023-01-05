import pygame


FGKJ:int  = 0
NOSR:int  = 1
intersections = {}
# vehicle typpes
CAR:str = 'car'
BUS:str = 'bus'
TRUCK:str = 'truck'
MOTORCYCLE:str = 'motorcycle'

# directions
RIGHT:str = 'right'
LEFT:str = 'left'
UP :str= 'up'
DOWN :str= 'down'



# Lanes
#Right direction lanes
CD = 0
IJ = 1
KL = 2
ST= 3
QR = 4
WX = 5

#Down direction lanes
A_I_ = 0
D_F_ = 1
J_Q_ = 2
L_N_ = 3
R_W_= 4
T_V_ = 5

#Left direction lanes
BA = 0
FE = 1
HG = 2
NM = 3
PO = 4
VU = 5

#Up direction lanes
E_C_ = 0
G_B_ = 1
M_K_ = 2
O_H_ = 3
X_P_ = 4
U_S_ = 5

# overall vehicles per lane
#lanes_quantity= [[0 for _ in range(6)] for _ in range(4)]
lanes_quantity = {
     RIGHT:[0,0,0,0,0,0],
     DOWN :[0,0,0,0,0,0],
     LEFT :[0,0,0,0,0,0],
     UP   :[0,0,0,0,0,0]
}
#lanes_quantity= [[ streets[direction][lane][] for lane in range(6)] for direction in range(4)]
# LOOK IN DESIG FILE
points = {
     'A' : { 'x' : 255 , 'y' : 5 },
     'B' : { 'x' : 360 , 'y' : 5 },

     'C' : { 'x' : 235 , 'y' : 25 },
     'D' : { 'x' : 360 , 'y' : 25 },

     'E' : { 'x' : 230 , 'y' : 250 },
     'F' : { 'x' : 335 , 'y' : 250 },
     'G' : { 'x' : 490 , 'y' : 250 },
     'H' : { 'x' : 620 , 'y' : 250 },

     'I' : { 'x' : 240 , 'y' : 275 },
     'J' : { 'x' : 355 , 'y' : 275 },
     'K' : { 'x' : 490 , 'y' : 275 },
     'L' : { 'x' : 620 , 'y' : 275 },

     'M' : { 'x' : 490  , 'y' : 505 },
     'N' : { 'x' : 610  , 'y' : 505 },
     'O' : { 'x' : 740  , 'y' : 505 },
     'P' : { 'x' : 870 , 'y' : 505 },

     'Q' : { 'x' : 490 , 'y' : 525 },
     'R' : { 'x' : 610 , 'y' : 525 },
     'S' : { 'x' : 740 , 'y' : 525 },
     'T' : { 'x' : 870 , 'y' : 525 },

     'U' : { 'x' : 730 , 'y' : 750 },
     'V' : { 'x' : 870 , 'y' : 750 },

     'W' : { 'x' : 730 , 'y' : 775 },
     'X' : { 'x' : 870 , 'y' : 775 },



     'A_' : { 'x' : 155 , 'y' : 80 },
     'B_' : { 'x' : 430 , 'y' : 80 },
     'C_' : { 'x' : 180 , 'y' : 80 },
     'D_' : { 'x' : 405 , 'y' : 80 },

     
     'I_' : { 'x' : 155 , 'y' : 215 },
     'E_' : { 'x' : 180 , 'y' : 215 },
     'F_' : { 'x' : 405 , 'y' : 215 },
     'G_' : { 'x' : 430 , 'y' : 215 },
     
     'H_' : { 'x' : 680 , 'y' : 340 },
     'J_' : { 'x' : 405 , 'y' : 340 },
     'K_' : { 'x' : 430 , 'y' : 340 },
     'L_' : { 'x' : 660 , 'y' : 340 },

     'O_' : { 'x' : 680  , 'y' : 430 },
     'M_' : { 'x' : 430  , 'y' : 430 },
     'N_' : { 'x' : 660  , 'y' : 430 },
     'Q_' : { 'x' : 405 , 'y' : 460 },

     'P_' : { 'x' : 930 , 'y' : 590 },
     'R_' : { 'x' : 660 , 'y' : 590 },
     'S_' : { 'x' : 680 , 'y' : 590 },
     'T_' : { 'x' : 915 , 'y' : 590 },

     'U_' : { 'x' : 680 , 'y' : 715 },
     'V_' : { 'x' : 915 , 'y' : 715 },
     'W_' : { 'x' : 660 , 'y' : 715 },
     'X_' : { 'x' : 930 , 'y' : 715 }


     
}


streets = {
     
     RIGHT:{         # RIGHT
          CD:{
               'x':[points['C']['x'] , points['D']['x']],
               'y':[points['C']['y'] , points['D']['y']] # y max
          },
          IJ:{
               'x':[points['I']['x'] , points['J']['x']],
               'y':[points['I']['y'] , points['J']['y']]
          },
          KL:{
               'x':[points['K']['x'] , points['L']['x']],
               'y':[points['K']['y'] , points['L']['y']]
          },
          ST:{
               'x':[points['S']['x'] , points['T']['x']],
               'y':[points['S']['y'] , points['T']['y']]
          },
          QR:{
               'x':[points['Q']['x'] , points['R']['x']],
               'y':[points['Q']['y'] , points['R']['y']]
          }
          ,
          WX:{
               'x':[points['W']['x'] , points['X']['x']],
               'y':[points['W']['y'] , points['X']['y']]
          }
     },
     LEFT:{         # LEFT
          BA:{
               'x':[points['B']['x'] , points['A']['x']],
               'y':[points['B']['y'] , points['A']['y']]
          },
          FE:{
               'x':[points['F']['x'] , points['E']['x']],
               'y':[points['F']['y'] , points['E']['y']]
          },
          HG:{
               'x':[points['H']['x'] , points['G']['x']],
               'y':[points['H']['y'] , points['G']['y']]
          },
          NM:{
               'x':[points['N']['x'] , points['M']['x']],
               'y':[points['N']['y'] , points['M']['y']]
          },
          PO:{
               'x':[points['P']['x'] , points['O']['x']],
               'y':[points['P']['y'] , points['O']['y']]
          },
          VU:{
               'x':[points['V']['x'] , points['U']['x']],
               'y':[points['V']['y'] , points['U']['y']]
          }
     },
     UP:{         # UP
          E_C_:{
               'x':[points['E_']['x'] , points['C_']['x']],
               'y':[points['E_']['y'] , points['C_']['y']]
          },
          G_B_:{
               'x':[points['G_']['x'] , points['B_']['x']],
               'y':[points['G_']['y'] , points['B_']['y']]
          },
          M_K_:{
               'x':[points['M_']['x'] , points['K_']['x']],
               'y':[points['M_']['y'] , points['K_']['y']]
          },
          O_H_:{
               'x':[points['O_']['x'],points['H_']['x']],
               'y':[points['O_']['y'],points['H_']['y']]
          },
          X_P_:{
               'x':[points['X_']['x'],points['P_']['x']],
               'y':[points['X_']['y'],points['P_']['y']]
          },
          U_S_:{
               'x':[points['U_']['x'],points['S_']['x']],
               'y':[points['U_']['y'],points['S_']['y']]
          }
     },
     DOWN:{         # DOWN
          A_I_:{
               'x':[points['A_']['x'],points['I_']['x']],
               'y':[points['A_']['y'],points['I_']['y']]
          },
          D_F_:{
               'x':[points['D_']['x'],points['F_']['x']],
               'y':[points['D_']['y'],points['F_']['y']]
          },
          J_Q_:{
               'x':[points['J_']['x'],points['Q_']['x']],
               'y':[points['J_']['y'],points['Q_']['y']]
          },
          L_N_:{
               'x':[points['L_']['x'],points['N_']['x']],
               'y':[points['L_']['y'],points['N_']['y']]
          },
          R_W_:{
               'x':[points['R_']['x'],points['W_']['x']],
               'y':[points['R_']['y'],points['W_']['y']]
          },
          T_V_:{
               'x':[points['T_']['x'],points['V_']['x']],
               'y':[points['T_']['y'],points['V_']['y']]
          }
     }
}

algorithm_active = False
# Font Size
font_size:int = 30

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
gray = (62,78,86)
gray_dark =(88,111,123)#(69,69,69)
gray_fatih = (188,197,202)


# Screensize
screen_width:int = 1100
screen_height:int = 800 #800
screen_size = (screen_width, screen_height)

# Loading signal images and font
#ronen change all image type to be with the image name , like this

red_signal_img_88= pygame.image.load('images/signals/red_88.png')
yellow_signal_img_88 = pygame.image.load('images/signals/yellow_88.png')
green_signal_88 = pygame.image.load('images/signals/green_88.png')


red_signal_img                = pygame.image.load('images/signals/red.png')
yellow_signal_img             = pygame.image.load('images/signals/yellow.png')
green_signal                  = pygame.image.load('images/signals/green.png')
non_signal                    = pygame.image.load('images/signals/non.png')
background                    = pygame.image.load('images/street.png')
background_white              = pygame.image.load('images/bg-white.png')
loading                       = pygame.image.load('images/loading.jpg')
data_analysis                 = pygame.image.load('images/data_analysis.png')
report                        = pygame.image.load('images/report.png')
current_config_downloading    = pygame.image.load('images/current_config_downloading.png')
overall_config_downloading    = pygame.image.load('images/overall_config_downloading.png')


# Default values of signal times
default_red :int = 150
default_yellow:int = 1
default_green:int = 10
default_minimum:int = 10
default_maximum:int = 60

# FGKJ_intersection.signals =[]
# FGKJ_intersection.number_of_signals :int = 4
sim_time :int = 15      # change this to change time of simulation
time_elapsed :int = 0

# Average times for vehicles to pass the intersection
car_time :int = 2
motorcycle_time :int = 1
bus_time :float = 2.5
truck_time :float = 2.5

# Red signal time at which cars will be detected at a signal
detection_time:int = 5

speeds = {}

# speeds:dict = {CAR: 2.25, BUS: 1.8, TRUCK: 1.8,
#           MOTORCYCLE: 2.5}  # average speeds of vehicles

vehicles_ = {
     
     RIGHT:{         # RIGHT
          CD:
               []
          ,
          IJ:
              []
          ,
          KL:
               []
          ,
          ST:
              []
          ,
          QR:
               []
          
          ,
          WX:
              []
          
     },
     LEFT:{         # LEFT
          BA:
              []
          ,
          FE:
              []
          ,
          HG:
               []
          ,
          NM:
              []
          ,
          PO:
               []
          ,
          VU:
               []
          
     },
     UP:{         # UP
          E_C_:
              []
          ,
          G_B_:
               []
          ,
          M_K_:
               []
          ,
          O_H_:
               []
          ,
          X_P_:
              []
          ,
          U_S_:
               []
          
     },
     DOWN:{         # DOWN
          A_I_:
             []
          ,
          D_F_:
               []
          ,
          J_Q_:
               []
          ,
          L_N_:
              []
          ,
          R_W_:
              []
          ,
          T_V_:
               []
          
     }
}

generating_coordinates = {
     
     RIGHT:{         # RIGHT
          CD: 
          {
               '1':[243,False],
               '0':[312,False],
          }
               
          ,
          IJ:
              {
               '1':[235,False],
               '0':[295,False],
          }
          ,
          KL:
               {
               '1':[500,False],
               '0':[583,False],
          }
          ,
          ST:
              {
               '1':[750,False],
               '0':[810,False],
          }
          ,
          QR:
               {
               '1':[490,False],
               '0':[560,False],
          }
          
          ,
          WX:
              {
               '1':[745,False],
               '0':[820,False],
          }
          
     },
     LEFT:{         # LEFT
          BA:
             {
               '1':[360,False],
               '0':[250,False],
          }
          ,
          FE:
              {
               '1':[356,False],
               '0':[250,False],
          }
          ,
          HG:
               {
               '1':[610,False],
               '0':[540,False],
          }
          ,
          NM:
              {
               '1':[610,False],
               '0':[515,False],
          }
          ,
          PO:
               {
               '1':[865,False],
               '0':[790,False],
          }
          ,
          VU:
               {
               '1':[865,False],
               '0':[790,False],
          }
          
     },
     UP:{         # UP
          E_C_:
              {
               '1':[205,False],
               '0':[130,False],
          }
          ,
          G_B_:
               {
               '1':[204,False],
               '0':[145,False],
          }
          ,
          M_K_:
               {
               '1':[460,False],
               '0':[400,False],
          }
          ,
          O_H_:
               {
               '1':[453,False],
               '0':[380,False],
          }
          ,
          X_P_:
              {
               '1':[715,False],
               '0':[647,False],
          }
          ,
          U_S_:
               {
               '1':[718,False],
               '0':[649,False],
          }
          
     },
     DOWN:{         # DOWN
          A_I_:
             {
               '1':[100,False],
               '0':[170,False],
          }
          ,
          D_F_:
               {
               '1':[100,False],
               '0':[170,False],
          }
          ,
          J_Q_:
               {
               '1':[350,False],
               '0':[425,False],
          }
          ,
          L_N_:
              {
               '1':[350,False],
               '0':[405,False],
          }
          ,
          R_W_:
              {
               '1':[600,False],
               '0':[680,False],
          }
          ,
          T_V_:
               {
               '1':[594,False],
               '0':[670,False],
          }
          
     }
}

steps_turning_vehicle:dict={
    
     CAR:{         
          RIGHT:{
               'left':[1.5,3],
               'right':[1.5,-1] 
          },
          DOWN:{
               'left':[-1,2.2],
               'right':[1.5,2.2] 
          },
          LEFT:{
               'left':[1.8,0.8],
               'right':[1.5,-1] 
          },
          UP:{
               'left':[3,-1],
               'right':[-0.5,-1] 
          }
     },
     BUS:{         
          RIGHT:{
               'left':[1.5,3],
               'right':[1.5,-1] 
          },
          DOWN:{
               'left':[-2,2.5],
               'right':[1,2.5] 
          },
          LEFT:{
               'left':[1.8,0.8],
               'right':[1.5,-1] 
          },
          UP:{
               'left':[3,-0.5],
               'right':[-0.5,-0.5] 
          }
     },
     TRUCK:{         
          RIGHT:{
               'left':[1.5,3],
               'right':[1.5,-1] 
          },
          DOWN:{
               'left':[-2,2.2],
               'right':[1,2.2] 
          },
          LEFT:{
               'left':[1.8,0.8],
               'right':[1.5,-1] 
          },
          UP:{
               'left':[3,-1],
               'right':[-0.5,-1] 
          }
     },
     MOTORCYCLE:{         
          RIGHT:{
               'left':[1.5,3],
               'right':[1.5,-1] 
          },
          DOWN:{
               'left':[-2,1.8],
               'right':[1,1.8] 
          },
          LEFT:{
               'left':[1.5,0.8],
               'right':[1.3,-1] 
          },
          UP:{
               'left':[3,-1.5],
               'right':[-0.5,-1.2] 
          }
     }


}
cars_number:int = 10
vehicles_generating:dict = {}


vehicle_types:dict = {
     0: CAR,
     1: BUS, 
     2: TRUCK, 
     3: MOTORCYCLE
     }


vehicles_weight = {}
    
direction_numbers = {0: RIGHT, 1: DOWN, 2: LEFT, 3: UP}


# Coordinates of stop lines
stop_lines:dict = {
     RIGHT: [370,635], 
     DOWN : [225,480], 
     LEFT : [493-55,745-55], 
     UP   : [340-55,592-70]
     }





default_stop:dict = {RIGHT: 580, DOWN: 320, LEFT: 810, UP: 545}
stops:dict = {RIGHT: [580, 580, 580], DOWN: [320, 320, 320],
         LEFT: [810, 810, 810], UP: [545, 545, 545]}

mid:dict = {
     RIGHT: {
          IJ:{
               'x': 407, 
               'y': 290
               },
          QR:{
               'x': 680, 
               'y': 525
               }    
          }, 
     DOWN: {
          IJ:{'x': 407, 'y': 290},
          QR:{'x': 680, 'y': 525}    
          }, 
     LEFT: {
          IJ:{'x': 407, 'y': 290},
          QR:{'x': 680, 'y': 525}    
          }, 
     UP: {
          IJ:{'x': 407, 'y': 290},
          QR:{'x': 680, 'y': 525}    
          },
     }

# rotate_factor = 70
# directly = {RIGHT: {'x': 705-rotate_factor, 'y': 445}, DOWN: {'x': 695, 'y': 450-rotate_factor},
#             LEFT: {'x': 695+rotate_factor - 20, 'y': 425}, UP: {'x': 695, 'y': 400+rotate_factor}}

rotate_point:dict = {
     RIGHT: { 
          # odd  represents short rotation
          # even represents long  rotation
          CD:350,
          KL:595,
          ST:850,
          WX:860 #
     },
     DOWN: {
     # odd  represents short rotation
          # even represents long  rotation
          A_I_:195, #
          J_Q_:425, #
          R_W_:695, #
          T_V_:685
     },
     LEFT: {
          # odd  represents short rotation
          # even represents long  rotation
          BA:205, #
          FE:225,
          NM:480,
          VU:725
     }, 
     UP: {
          # odd  represents short rotation
          # even represents long  rotation
          X_P_:590, #
          O_H_:350, #
          G_B_:95, #
          E_C_:100
     }
     }
   
rotation_angle = 3
next_lane_of = {
     
     RIGHT:{        
          CD:[ DOWN , D_F_ ],
          KL:[ DOWN , L_N_ ],
          ST:[ DOWN , T_V_ ],
          WX:[ UP   , X_P_ ],
          #
          IJ:[ RIGHT, KL   ],
          QR:[ RIGHT, ST   ]      

     },
     LEFT:{        
          BA:[ DOWN , A_I_ ],
          FE:[ UP   , E_C_ ],
          NM:[ UP   , M_K_ ],
          VU:[ UP   , U_S_ ],
          #
          HG:[ LEFT, FE   ],
          PO:[ LEFT, NM   ]      
     },
     UP:{       
          E_C_:[ RIGHT , CD ],
          G_B_:[ LEFT  , BA ],
          O_H_:[ LEFT  , HG ],
          X_P_:[ LEFT  , PO ],
          #
          U_S_:[ UP, O_H_],
          M_K_:[ UP, G_B_]    
          
     },
     DOWN:{        
          A_I_:[ RIGHT , IJ ],
          J_Q_:[ RIGHT , QR ],
          R_W_:[ RIGHT , WX ],
          T_V_:[ LEFT  , VU ],
          #
          D_F_:[ DOWN, J_Q_],
          L_N_:[ DOWN, R_W_]    
     }
}
intersection_weights_for_lanes = {
     FGKJ : {
          
          RIGHT :[IJ ,A_I_],
          DOWN  :[D_F_,CD],
          LEFT  :[HG,O_H_],
          UP    :[M_K_ ,NM],
     },
     NOSR:{
          RIGHT :[QR ,J_Q_],
          DOWN  :[L_N_,KL],
          LEFT  :[PO ,X_P_],
          UP    :[U_S_,VU],
     }
}
intersection_lanes = {
     FGKJ : {
          
          RIGHT :[IJ  ],
          DOWN  :[D_F_],
          LEFT  :[HG],
          UP    :[M_K_ ],
     },
     NOSR:{
          RIGHT :[QR  ],
          DOWN  :[L_N_],
          LEFT  :[PO  ],
          UP    :[U_S_],
     }
}

# how many vehicles crossed in each signal
crossed = {
     FGKJ : {

          RIGHT :{
               'crossed': 0
          },
          DOWN  :{
               'crossed': 0
          },
          LEFT  :
          {
               'crossed': 0
          },
          UP    :{
               'crossed': 0
          }
     },
     NOSR:{
          RIGHT :{
               'crossed': 0
          },
          DOWN  :{
               'crossed': 0
          },
          LEFT  :{
               'crossed': 0
          },
          UP    :{
               'crossed': 0
          }
     }
}
# Gap between vehicles
gap  = 12   # stopping gap
gap2 = 12   # moving gap






circle_params_for_rotation = {
     RIGHT:{         # RIGHT
            CD:[0,-1, 1,-1],
            KL:[0,-1, 1,-1],
            ST:[0,-1, 1,-1],
            WX:[0, 1,-1, 1]
     },
     LEFT:{  
            BA:[0,-1,-1, 1],
            FE:[0, 1, 1,-1],
            NM:[0, 1, 1,-1],
            VU:[0, 1, 1,-1]
     },
     UP:{     
          E_C_:[-1,0, 1,-1],
          G_B_:[ 1,0,-1, 1],
          O_H_:[ 1,0,-1, 1],
          X_P_:[ 1,0,-1, 1]
     },
     DOWN:{   
          A_I_:[-1,0,-1, 1],  
          J_Q_:[-1,0,-1, 1],
          R_W_:[-1,0,-1, 1],
          T_V_:[ 1,0, 1,-1]      
     }
}



circle_coordinates = {
     
     RIGHT:{ #        # RIGHT
          CD: 
          {
               'pos':(370,83),
               'radius':45
          }
               
          ,
          KL:{
               'pos':(616,335),
               'radius':50
          }
          ,
          ST:{
               'pos':(873,581),
               'radius':46
          }
          
          ,
          WX:{
               'pos':(880,722),
               'radius':63
          }
          
     },
     LEFT:{ #        # LEFT
          BA:
              {
          #      'pos':(225,80),
          #      'radius':63
          
               'pos':(225,80),
               'radius':65
          }
          ,
          FE:
              {
               'pos':(237,217),
               'radius':42
          }
          ,
         
          NM:
              {
               'pos':(500,449),
               'radius':61
          }
          ,
          VU:
               {
              'pos':(742,715),
               'radius':45
          }
          
     },
     UP:{         # UP
          E_C_:
              {
               'pos':(249,90),
               'radius':58
          }
          ,
          G_B_:
               {
               'pos':(375,80),
               'radius':65
          }
          ,
          
          O_H_:
               {
               'pos':(625,328),
               'radius':65
          }
          ,
          X_P_:
              {
               'pos':(872,573),
               'radius':65
          }
          
     },
     DOWN:{         # DOWN
          A_I_:
             {
               'pos':(230,220),
               'radius':67
          }
          ,
          
          J_Q_:
               {
               'pos':(500,453),
               'radius':83
          }
          ,
          R_W_:
              {
               'pos':(731,720),
               'radius':65
          }
          ,
          T_V_:
               {
               'pos':(870,705),
               'radius':52
          }
          
     }
}


