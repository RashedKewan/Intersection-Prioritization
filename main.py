import os
import shutil
import threading
import time
import pygame
import Simulation as sim
import sys
import GlobalData as GD
import FileController as fc
import PDFReport as pdf
from reportlab.pdfgen import canvas
import openpyxl

def run_thread(thread_name:str , thread_target,args=()):
    thread = threading.Thread(name=thread_name, target=thread_target, args=args)
    thread.daemon = True
    thread.start()
    return thread





screen = pygame.display.set_mode(GD.screen_size)
pygame.display.set_caption("SIMULATION")
font = pygame.font.Font(None, GD.font_size)

def turn_signal_on(intersection :int, signal_img, index:int):
    screen.blit(signal_img, GD.intersections[intersection].signal_coordinates[index])




def display_signal_timer_and_vehicle_count_for_each_signal(intersection :int, signal_number:int , signal_texts : list ):
        signal_texts[signal_number] = font.render(str(GD.intersections[intersection].signals[signal_number].signal_text), True, GD.white, GD.black)
        screen.blit(signal_texts[signal_number], GD.intersections[intersection].signal_timer_coordinates[signal_number])
        
        displayText = GD.crossed[intersection][GD.direction_numbers[signal_number]]['crossed']
        #displayText = GD.vehicles_[GD.direction_numbers[signal_number]]['crossed']
        GD.intersections[intersection].vehicle_count_texts[signal_number] = font.render(str(displayText), True, GD.black, GD.white)
        screen.blit(GD.intersections[intersection].vehicle_count_texts[signal_number], GD.intersections[intersection].vehicle_count_coordinates[signal_number])
        

def display_the_vehicles():
    for vehicle in sim.simulation:
        #screen.blit(vehicle.current_image, [vehicle.x, vehicle.y])
        vehicle.move_(screen)


def display_time_elapsed():
    algorithm_activity = 'OFF'
    if(GD.algorithm_active):
        algorithm_activity = 'ON'
    time_elapsed_text = font.render(f"Algorithm Activity Status  : {algorithm_activity} ", True, GD.black, GD.white)
    screen.blit(time_elapsed_text, (750, 20))
    time_elapsed_text = font.render(("Time Elapsed: " + str(GD.time_elapsed)), True, GD.black, GD.white)
    screen.blit(time_elapsed_text, (750, 50))
    


def signals_conroller(intersection):
            traffic_sign_arrow_images = []

            for dir in GD.direction_numbers.values():
                traffic_sign_arrow_images.append(pygame.image.load(f'images/traffic_signs/{dir}.png'))
            
            for i,coordinate in enumerate(GD.intersections[intersection].traffic_sign_arrow_coordinates):
                screen.blit(traffic_sign_arrow_images[i], (coordinate[0], coordinate[1]))



            for i in range(0, GD.intersections[intersection].number_of_signals):
                if(i == GD.intersections[intersection].current_green):
                    if(GD.intersections[intersection].current_yellow == 1):
                        GD.intersections[intersection].signals[i].signal_text = GD.intersections[intersection].signals[i].yellow
                        turn_signal_on(intersection ,signal_img=GD.yellow_signal_img, index=i)

                        
                    else:
                        GD.intersections[intersection].signals[i].signal_text = GD.intersections[intersection].signals[i].green
                        if(GD.intersections[intersection].signals[i].green <= 6 and GD.intersections[intersection].signals[i].green > 0 and GD.intersections[intersection].signals[i].green % 2 == 0):
                            turn_signal_on(intersection ,signal_img = GD.non_signal, index=i)
                            
                        elif(GD.intersections[intersection].signals[i].green <= 6 and GD.intersections[intersection].signals[i].green > 0 and GD.intersections[intersection].signals[i].green % 2 == 1):
                            turn_signal_on(intersection ,signal_img = GD.green_signal, index=i)
                        
                        else :
                            turn_signal_on(intersection ,signal_img = GD.green_signal, index=i)
        
                else:
                    # if(GD.intersections[intersection].signals[i].red  < 5 and i == GD.intersections[intersection].next_green):
                    #     GD.intersections[intersection].signals[i].signal_text = GD.intersections[intersection].signals[i].red 
                    # elif(i != GD.intersections[intersection].next_green or i != GD.intersections[intersection].current_green):
                    if(i != GD.intersections[intersection].current_green):
                        GD.intersections[intersection].signals[i].signal_text = ""
                    turn_signal_on(intersection , signal_img = GD.red_signal_img, index=i)
                

            signal_texts = ["", "", "", ""]
            for i in range(0, GD.intersections[intersection].number_of_signals):
                display_signal_timer_and_vehicle_count_for_each_signal(intersection ,signal_number = i , signal_texts = signal_texts)



    
def output():
    # Check if the directory exists
    if not os.path.exists('temp'):
        # Create the directory
        os.makedirs('temp')
        
    path , current_time = fc.create_directory()
    fc.create_xlsx_file()
    for vehicle in sim.simulation:
        data = { 
            'vehicle_type':vehicle.vehicle_class, 
            'vehicle_speed_avg':vehicle.speed_avg
            }
        fc.append_dict_to_xlsx( filename= 'vehicles_avg_speeds.xlsx' , data=data  )
    if(len(sim.simulation) <= 0):
        data = { 
            'vehicle_type':"", 
            'vehicle_speed_avg':0
            }
        fc.append_dict_to_xlsx( filename= 'vehicles_avg_speeds.xlsx' , data=data  )
    # Plot the average speeds for the specified vehicle types
    fc.plot_average_speeds_for_each_vehicle_type()
    fc.plot_vehicle_average_speed()
    pdf.create_report(path , current_time)
   

def to_percent(fraction):
    percent = int(round(fraction * 100))
    return f"{percent}%" , percent

def create_text(displayText , position, font_size,font_color):
    # Create the font object with the specified size
    font = pygame.font.Font(None, font_size)

    # Create the text surface
    text_surface = font.render(displayText, True, font_color)

    # Get the rectangle for the text surface
    text_rect = text_surface.get_rect()

    # Set the position of the text rectangle
    text_rect.center = position 

    # Draw the text to the screen
    screen.blit(text_surface, text_rect) 

def show_loading_report():
    temp =  GD.sim_time -5  
    while(GD.sim_time > GD.time_elapsed ):
        screen.blit(GD.background_white, (0, 0))
        displayText , percent = to_percent(( GD.time_elapsed - GD.sim_time ) / (temp))
        displayText = 100 + 2*percent
        create_text(f'Loading Report {displayText}%' , ( 560,70) ,50,GD.black)
        screen.blit(GD.report, (337, 125))
        pygame.display.update()


###############################################################################################################################
###############################################################################################################################
###############################################################################################################################

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
gray = (62,78,86)
gray_dark =(88,111,123)#(69,69,69)

# Set the dimensions of the dropdown menu
menu_width = 75
menu_height = 25




# Create the options for the dropdown menu
options = ["On", "Off"]

def read_algorithm_activity():
    # Open the workbook and sheet
    workbook = openpyxl.load_workbook("configuration/Algorithm.xlsx")
    sheet = workbook["Sheet1"]
    if( sheet.cell(row=1, column=2).value.lower()  == 'true'):
        return  options[0]
    return  options[1]



def read_simulation_time():
    # Open the workbook and sheet
    workbook = openpyxl.load_workbook("configuration/Simulation.xlsx")
    sheet = workbook["Sheet1"]
    return str(sheet.cell(row=1, column=2).value)
    

# Set the default option
default_option = read_algorithm_activity()

# Open the Excel workbook
workbook = openpyxl.load_workbook('configuration/vehicles_db.xlsx')

# Get the first worksheet
worksheet = workbook['Sheet1']

# Define some constants for the table layout
TABLE_TOP = 100
TABLE_LEFT = 75
TABLE_WIDTH = 1000
TABLE_HEIGHT = 600
CELL_WIDTH = TABLE_WIDTH // 5
CELL_HEIGHT = TABLE_HEIGHT // 6

class DropdownMenu:
    def __init__(self, width, height, options, default_option, font):
        self.width = width
        self.height = height
        self.options = options
        self.default_option = default_option
        self.font = font
        self.selected_option = default_option
        self.menu_open = False

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        # Draw the dropdown box
         # Draw the dropdown box
        pygame.draw.rect(screen, gray, (self.x, self.y, self.width, self.height),1)

        # Render the selected option
        text = self.font.render(self.selected_option, 1, gray)
        screen.blit(text, (self.x + 10, self.y ))

        # If the menu is open, draw the options
        if self.menu_open:
            y = self.y + self.height
            for option in self.options:
                # Render the option
                text = self.font.render(option, 1, gray)
                screen.blit(text, (self.x + 10, y ))
                # Increment the y position for the next option
                y += self.height

    def toggle_menu(self):
        self.menu_open = not self.menu_open

    def is_mouse_selection(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            return True
        return False

    def set_menu_selection(self, pos):
        if self.menu_open:
            y = self.y + self.height
            for option in self.options:
                if pos[1] > y and pos[1] < y + self.height:
                    self.selected_option = option
                    self.menu_open = False
                y += self.height





font = pygame.font.SysFont('Arial', 22)
# Set the font and the font size
#font = pygame.font.Font(None, 32)
# Create the dropdown menu
menu = DropdownMenu(menu_width, menu_height, options, default_option, font)

# Set the position of the dropdown menu
menu_x = TABLE_WIDTH-50-menu_width
menu_y = 40
menu.set_position(menu_x, menu_y)




# Create a font for the table cells
#font = pygame.font.Font(None, font_size)

# Create a surface to draw the table on
table_surface = pygame.Surface((TABLE_WIDTH, TABLE_HEIGHT))



# Define the input rectangle
input_rect = pygame.Rect(TABLE_LEFT+270,40, 75, 25)

# Set up the font and text surface
#font = pygame.font.Font(None, 32)
text_surface = font.render(read_simulation_time(), True, (255, 255, 255))
# Set up the input string
input_string = read_simulation_time()





def create_text(displayText , position, font_size,font_color):
    # Create the font object with the specified size
    font = pygame.font.SysFont('Arial', 22)

    # Create the text surface
    text_surface = font.render(displayText, True, font_color)

    # Get the rectangle for the text surface
    text_rect = text_surface.get_rect()

    # Set the position of the text rectangle
    text_rect.center = position 

    # Draw the text to the screen
    screen.blit(text_surface, text_rect)







def create_save_button():
    """Create the Save button and its surface."""
    global save_button, save_button_surface

    # Create the Save button
    save_button = pygame.Rect(TABLE_LEFT, TABLE_TOP + TABLE_HEIGHT + 10, CELL_WIDTH , 50)
    save_button_text = font.render('Save', True, (255, 255, 255))

    # Create the surface to display the Save button on
    save_button_surface = pygame.Surface((CELL_WIDTH, 50))
    save_button_surface.fill(gray_dark)
    save_button_surface.blit(save_button_text, (CELL_WIDTH // 2 - save_button_text.get_width() // 2, 25 - save_button_text.get_height() // 2))



def create_start_button():
    """Create the start button and its surface."""
    global start_button, start_button_surface

    # Create the Save button
    start_button = pygame.Rect(TABLE_LEFT+TABLE_HEIGHT+150, TABLE_TOP + TABLE_HEIGHT + 10, CELL_WIDTH , 50)
    start_button_text = font.render('Srart Simulation', True, (255, 255, 255))

    # Create the surface to display the Start button on
    start_button_surface = pygame.Surface((CELL_WIDTH, 50))
    start_button_surface.fill(gray_dark)
    start_button_surface.blit(start_button_text, (CELL_WIDTH // 2 - start_button_text.get_width() // 2, 25 - start_button_text.get_height() // 2))






def draw_table():
    """Draw the table and its cells."""
    global table_surface

    # Draw the table
    table_surface.fill(white)
    for row in range(5):
        for col in range(4):
            # Calculate the cell rect
            cell_rect = pygame.Rect(TABLE_LEFT + col * CELL_WIDTH, TABLE_TOP + row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
           
            # Draw the cell rect
            pygame.draw.rect(table_surface, gray, cell_rect, 1)
            # Render the cell text
            text = table[row][col]
            cell_text = font.render((str(text)).encode('utf-8'), True, gray)
            # Calculate the position of the cell text
            cell_text_pos = (TABLE_LEFT + col * CELL_WIDTH + CELL_WIDTH // 2 - cell_text.get_width() // 2, TABLE_TOP + row * CELL_HEIGHT + CELL_HEIGHT // 2 - cell_text.get_height() // 2)
            # Draw the cell text
            table_surface.blit(cell_text, cell_text_pos)






def set_algorithm_activity(is_active : bool = False):
    # Open the workbook and sheet
    workbook = openpyxl.load_workbook("configuration/Algorithm.xlsx")
    sheet = workbook["Sheet1"]

    # Define the new column name
    new_column_name = f"{is_active}"
    # Update the value of the cell
    sheet.cell(row=1, column=2).value = new_column_name

   
    
    try:
         # Save the changes to the workbook
        workbook.save("configuration/Algorithm.xlsx")
        print("algorithm_activity saved successfully")
        return True
    except Exception as e:
        print("Error saving algorithm_activity:", e)
        return False


def set_simulation_time(sim_time:int = 15):
    # Open the workbook and sheet
    workbook = openpyxl.load_workbook("configuration/Simulation.xlsx")
    sheet = workbook["Sheet1"]

    # Define the new column name
    new_column_name = f"{sim_time}"
    # Update the value of the cell
    sheet.cell(row=1, column=2).value = new_column_name

   
    try:
         # Save the changes to the workbook
        workbook.save("configuration/Simulation.xlsx")
        print("simulation_time saved successfully")
        return True
    except Exception as e:
        print("Error saving simulation_time:", e)
        return False



def handle_save_message(msg , color):
    timer = 500
    
    while(timer > 0):
        # Create the font object with the specified size
        font = pygame.font.Font(None, 30)

        # Create the text surface
        text_surface = font.render(f"                                                                         {msg}                                                                         ", True, (255,255,255),color)

        # Get the rectangle for the text surface
        text_rect = text_surface.get_rect()

        # Set the position of the text rectangle
        text_rect.center = (550,10) 

        # Draw the text to the screen
        screen.blit(text_surface, text_rect)
        timer -=1
        


def save_table():
    vehicles_db_saved = False
    """Save the values in the table to the Excel workbook."""
    for row in range(1, 6):
        for col in range(1, 5):
            # Set the cell value in the worksheet
            worksheet.cell(row=row, column=col, value=table[row-1][col-1])
    
    try:
        # Save the changes to the workbook
        workbook.save('configuration/vehicles_db.xlsx')
        print("Workbook saved successfully")
        vehicles_db_saved = True
    except Exception as e:
        print("Error saving workbook:", e)
       
    active = False
    if(menu.selected_option == 'On'):
        active = True
    algorithm_activity_saved = set_algorithm_activity(is_active=active)
    simulation_time_saved = set_simulation_time(sim_time= int(input_string))
    if(algorithm_activity_saved and simulation_time_saved and vehicles_db_saved):
        run_thread(thread_name='handle_save_message', thread_target= handle_save_message,args=("Your changes have been saved!",(111,149,111)))
    else:
        run_thread(thread_name='handle_save_message', thread_target= handle_save_message,args=("Your changes failed to save!",(255,99,71)))
   





# Initialize the table with the values from the worksheet
table = []
for row in worksheet.iter_rows():
    table_row = []
    for cell in row:
        table_row.append(cell.value)
    table.append(table_row)

# Create the Save button and its surface
create_save_button()
create_start_button()
background_white = pygame.image.load('images/bg-white.png')
# Run the game loop
def init():
    global input_string
    running = True
    input_enabled = False
    while running:
        screen.blit(background_white, (0, 0))
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    # Handle mouse button down events
                    if event.button == 1:
                        # Left mouse button clicked
                        # Enable input
                        input_enabled = True
                    elif event.button == 3:
                        # Right mouse button clicked
                        # Disable input
                        input_enabled = False
                if menu.is_mouse_selection(event.pos):
                    menu.toggle_menu()
                    print(menu.selected_option)
                else:
                    menu.set_menu_selection(event.pos)
                    print(menu.selected_option)
                # Check if the Save button was clicked
                if save_button.collidepoint(event.pos):
                    save_table()
                elif start_button.collidepoint(event.pos):
                    screen.fill((255, 255, 255))
                    running = False
                else:
                    # Check which cell was clicked
                    row = (event.pos[1] - TABLE_TOP) // CELL_HEIGHT
                    row -= 1
                    col = (event.pos[0] - TABLE_LEFT) // CELL_WIDTH
                    print(f"row {row }  col {col}")
                    if row > 0 and row < 5 and col > 0 and col < 4:
                        current_row = row
                        current_col = col
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if(input_enabled):
                        input_string = input_string[:-1]
                    else:
                        # Delete the character before the cursor in the current cell
                        table[current_row][current_col] = str(table[current_row][current_col])[:-1]
                elif event.unicode.isprintable():
                    number = ["0","1","2","3","4","5","6","7","8","9"]
                    if((event.unicode) in number and input_enabled):
                        if( len(input_string) <5):
                            input_string += event.unicode
                    else:
                        num = str(table[current_row][current_col])
                        
                        if(current_col == 1):
                            if "." not in num and ((event.unicode) in number or event.unicode == ".") and len(num) > 0 or ("." in num and (event.unicode) in number) or "." not in num and (event.unicode) in number and len(num) == 0:
                                num += event.unicode
                                table[current_row][current_col] = float(num)
                        else:
                            if((event.unicode) in number):
                                num += event.unicode
                                table[current_row][current_col] = int(num)
                    

                

        
        # Draw the table and the Save button
        draw_table()
        screen.blit(save_button_surface, save_button)
        screen.blit(start_button_surface, start_button)
        # Draw the table surface on the window
        screen.blit(table_surface, (TABLE_LEFT, TABLE_TOP))
        create_text('Algorithm Activity Status : ', (menu_x-130,50) ,32,gray)
        # Draw the dropdown menu
        menu.draw(screen)


        create_text('Simulation Time : ', (250,50) ,32,gray)
        # Update the text surface with the input string
        text_surface = font.render(input_string, True, gray)
        # Draw the input rectangle to the screen
        pygame.draw.rect(screen, gray_dark, input_rect, 1)
        # Draw the text surface to the screen
        screen.blit(text_surface, input_rect.topleft)

        pygame.display.update()
###############################################################################################################################
###############################################################################################################################
###############################################################################################################################
class Main:
    init()
    GD.sim_time        = fc.read_xlsx_file_for_sim()+5
    algorithm_activity = fc.read_xlsx_file_for_algo()
    if( algorithm_activity.lower() == 'true'):
        GD.algorithm_active = True

    GD.vehicles_generating  = fc.read_xlsx_file(directory = 'configuration' , filename = 'vehicles_db.xlsx',column='generating_number')
    GD.vehicles_weight      = fc.read_xlsx_file(directory = 'configuration' , filename = 'vehicles_db.xlsx',column='weight')
    GD.speeds               = fc.read_xlsx_file(directory = 'configuration' , filename = 'vehicles_db.xlsx',column='speed')
   
    cars_number:int = 0
    for v in GD.vehicles_generating.values():
        cars_number += v
    GD.cars_number = cars_number
    run_thread("generateVehicles" ,sim.generate_vehicle)
 
    while(GD.cars_number > 0):
        screen.blit(GD.loading, (0, 0))
        
        # Set the font and font size
        font = pygame.font.Font(None, 36)
        displayText,percent =to_percent((cars_number - GD.cars_number ) / cars_number)
        
        if(percent < 60):
            screen.blit(GD.red_signal_img_88, (350, 300))
        elif(percent >= 60 and percent < 90 ):
            create_text('Get Ready!' , ( 560,100) ,50,GD.white)
            screen.blit(GD.yellow_signal_img_88, (350, 300))
        elif(percent >= 90 ):
            create_text('Go!' , ( 580,100) ,50,GD.white)
            screen.blit(GD.green_signal_88 , (350, 300))

        
        create_text(displayText , ( 550,390) ,32,GD.white)
        
        pygame.display.update()   

    #########################################################################################################################
    ####################################################    Threads   #######################################################
    #########################################################################################################################
    run_thread(thread_name="simulationTime" ,thread_target=sim.simulation_time)
    run_thread("initialization" ,sim.initialize)
   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if(GD.time_elapsed == GD.sim_time-5):
            t1  = run_thread("show_loading_report" , show_loading_report)
            t2  = run_thread("output" , output)
            t1.join()
            t2.join()
            sys.exit()
            
        
       
    #########################################################################################################################
    #######################################      Display Background In Simulation     #######################################
    #########################################################################################################################
        screen.blit(GD.background_white, (0, 0))
        screen.blit(GD.background, (150, 0))   
        #mouse coordination
        # mousex, mousey = pygame.mouse.get_pos()
        # print(f"{mousex} , {mousey}")

    #########################################################################################################################
    #######################################  display signal and set timer according   #######################################
    #######################################  to current status: green, yello, or red  #######################################
    #########################################################################################################################
        run_thread(thread_name="FGKJ signals_conroller" ,thread_target=signals_conroller,args=(GD.FGKJ,)).join()
        run_thread(thread_name="NOSR signals_conroller" ,thread_target=signals_conroller,args=(GD.NOSR,)).join()
    
        
        display_time_elapsed()

        display_the_vehicles()
        pygame.display.update()



