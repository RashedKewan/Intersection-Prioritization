from openpyxl import load_workbook
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
import GlobalData as GD





# Function to convert a table from an Excel file to an image
def excel_to_image(filename):
    # Open the Excel file
    wb = load_workbook(filename)
    ws = wb.active

    # Select the table
    table = []
    for row in ws.iter_rows(min_row=1, max_col=ws.max_column, max_row=ws.max_row):
        table.append([cell.value for cell in row])

    # Convert the table to an image
    font = ImageFont.truetype("arial.ttf", 12)
    img_width = 500
    img_height = len(table) * 20
    image = Image.new("RGB", (img_width, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    y_offset = 0
    for row in table:
        x_offset = 0
        for cell in row:
            draw.text((x_offset, y_offset), str(cell), font=font, fill=(0, 0, 0))
            x_offset += 150
        y_offset += 20

    # Save the image
    img = filename.replace(".xlsx", ".png")
    img = img.rsplit("/", 1)[-1]
    image.save(f"temp/{img}")
    return img_height


def create_report(path , current_time):
    # Convert the tables from the Excel files to images
    vehicles_data_image_height = excel_to_image(filename='configuration/vehicles_data.xlsx')

    #Create a new PDF document with a size of letter paper
    pdf_file = f"{path}/report.pdf"
    pdf_canvas = Canvas(pdf_file, pagesize=letter)
    y = 750

    # Title

    # Set the font
    pdf_canvas.setFont("Helvetica", 24)

    # Set the fill color to black
    pdf_canvas.setFillColorRGB(0, 0, 0)
    pdf_canvas.drawString(50, y, "Prioritize The Passage Of Vehicles At Intersections")
    y = y - 25
    pdf_canvas.drawString(150, y, "According To Fuel Consumption")
    y = y - 30
    pdf_canvas.drawString(250, y, "-  Report  -")
    y = y - 40

    
    # Set the font
    pdf_canvas.setFont("Helvetica", 12)
    # Set the fill color to black
    pdf_canvas.setFillColorRGB(0, 0, 0)
    # Date
    time = current_time.rsplit("/", 1)[1]
    time = time.replace('-',':')
    date = current_time.rsplit("/", 1)[0]
    date = date.replace("-","/")

    pdf_canvas.drawString(50, y, f"Date : {date}")
    pdf_canvas.drawString(50, y-15, f"Time : {time}")

    # Algorithm
    algorithm_activity = 'OFF'
    if( GD.algorithm_active ):
        algorithm_activity = 'ON'
    pdf_canvas.drawString(400, y   , f"Algorithm Activity Status : {algorithm_activity}")
    pdf_canvas.drawString(400, y-15, f"Time Elapsed                  : {GD.time_elapsed}")
    

    y = y - 130
    # excel files
    pdf_canvas.drawString(50, y, "_____________________________    Vehicles Data    _____________________________")
    y = y - 150
    pdf_canvas.drawImage("temp/vehicles_data.png", 50, y, 480, vehicles_data_image_height)
    # y = y - 25
    # pdf_canvas.drawString(50, y, "________________________________________________________")
    # y = y - 25 - vehicles_speed_image_height
    # pdf_canvas.drawImage("temp/vehicles_speed.png", 50, y, 500, vehicles_speed_image_height)
    # y = y - 25
    # pdf_canvas.drawString(50, y, "________________________________________________________")
    # y = y - 25 - vehicles_weight_image_height
    # pdf_canvas.drawImage("temp/vehicles_weight.png", 50, y, 500, vehicles_weight_image_height)
    
    pdf_canvas.showPage()
    # Add the plot image to the PDF document
    y = 750
    pdf_canvas.drawString(100, y, "___________________________    Graphs    ___________________________")
    pdf_canvas.drawImage("temp/average_speeds_for_each_type.png", x=100, y=410, width=400, height=300)
    pdf_canvas.drawImage("temp/avg_speed_for_each_vehicle.png", x=100, y=110, width=400, height=300)
    pdf_canvas.showPage()
    pdf_canvas.save()
    print('Report Created.')