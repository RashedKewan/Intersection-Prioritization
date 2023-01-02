import openpyxl
import pygame
import subprocess



pygame.init() 
# Open the Excel workbook
workbook = openpyxl.load_workbook('configuration/vehicles_db.xlsx')

# Get the first worksheet
worksheet = workbook['Sheet1']

# Define some constants for the table layout
TABLE_TOP = 25
TABLE_LEFT = 75
TABLE_WIDTH = 1000
TABLE_HEIGHT = 700
CELL_WIDTH = TABLE_WIDTH // 5
CELL_HEIGHT = TABLE_HEIGHT // 6


# Colours
black = (0, 0, 0)
white = (255, 255, 255)

# Screensize
screen_width:int = 1100
screen_height:int = 800 #800
screen_size = (screen_width, screen_height)
# Create the window and set its size
window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("SIMULATION")
font_size:int = 30
font = pygame.font.SysFont('Arial', 30)

# Create a font for the table cells
font = pygame.font.Font(None, font_size)

# Create a surface to draw the table on
table_surface = pygame.Surface((TABLE_WIDTH, TABLE_HEIGHT))

def create_save_button():
    """Create the Save button and its surface."""
    global save_button, save_button_surface

    # Create the Save button
    save_button = pygame.Rect(TABLE_LEFT, TABLE_TOP + TABLE_HEIGHT + 10, CELL_WIDTH, 50)
    save_button_text = font.render('Save', True, (255, 255, 255))

    # Create the surface to display the Save button on
    save_button_surface = pygame.Surface((CELL_WIDTH, 50))
    save_button_surface.fill((0, 0, 255))
    save_button_surface.blit(save_button_text, (CELL_WIDTH // 2 - save_button_text.get_width() // 2, 25 - save_button_text.get_height() // 2))

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
            pygame.draw.rect(table_surface, black, cell_rect, 1)
            # Render the cell text
            text = table[row][col]
            cell_text = font.render((str(text)).encode('utf-8'), True, black)
            # Calculate the position of the cell text
            cell_text_pos = (TABLE_LEFT + col * CELL_WIDTH + CELL_WIDTH // 2 - cell_text.get_width() // 2, TABLE_TOP + row * CELL_HEIGHT + CELL_HEIGHT // 2 - cell_text.get_height() // 2)
            # Draw the cell text
            table_surface.blit(cell_text, cell_text_pos)

def save_table():
    """Save the values in the table to the Excel workbook."""
    for row in range(1, 6):
        for col in range(1, 5):
            # Set the cell value in the worksheet
            worksheet.cell(row=row, column=col, value=table[row-1][col-1])
    # Save the changes to the workbook
    workbook.save('configuration/vehicles_db.xlsx')
    print('saved')

# Initialize the table with the values from the worksheet
table = []
for row in worksheet.iter_rows():
    table_row = []
    for cell in row:
        table_row.append(cell.value)
    table.append(table_row)

# Create the Save button and its surface
create_save_button()
background_white = pygame.image.load('images/bg-white.png')
# Run the game loop
running = True
while running:
    window.blit(background_white, (0, 0))
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the Save button was clicked
            if save_button.collidepoint(event.pos):
                save_table()
            else:
                # Check which cell was clicked
                row = (event.pos[1] - TABLE_TOP) // CELL_HEIGHT
                col = (event.pos[0] - TABLE_LEFT) // CELL_WIDTH
                print(f"row {row }  col {col}")
                if row > 0 and row < 5 and col > 0 and col < 4:
                    current_row = row
                    current_col = col
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Delete the character before the cursor in the current cell
                table[current_row][current_col] = str(table[current_row][current_col])[:-1]
            elif event.unicode.isprintable():
                num = str(table[current_row][current_col])
                number = ["0","1","2","3","4","5","6","7","8","9"]
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
    window.blit(save_button_surface, save_button)
    # Draw the table surface on the window
    window.blit(table_surface, (TABLE_LEFT, TABLE_TOP))
    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
subprocess.run(["python", "main.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)