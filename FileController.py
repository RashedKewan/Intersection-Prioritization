import os
import shutil
import matplotlib.pyplot as plt
import pandas as pd
import GlobalData as GD
import openpyxl
import datetime
import shutil
import Simulation as sim

def copy_file(src ,dst):
  # Copy the file from the source to the destination
  shutil.copy(src, dst)



def get_current_time():
  now = datetime.datetime.now()
  date_time = now.strftime("%d-%m-%Y/%H-%M-%S")
  return date_time




def read_xlsx_file_for_sim(directory = 'configuration' , filename = 'Simulation.xlsx'):
  file_path = f"{directory}/{filename}"

  # Open the workbook
  workbook = openpyxl.load_workbook(file_path)

  # Get the sheet you want to access
  sheet = workbook['Sheet1']

  # Iterate over the columns in the sheet
  for i,col in enumerate(sheet.columns):
      # Find the column you want to access
      if i == 1:
          # Print the values in the column
          for cell in col:
            return int(cell.value)





def read_xlsx_file_for_algo(directory = 'configuration' , filename = 'Algorithm.xlsx'):
  file_path = f"{directory}/{filename}"

  # Open the workbook
  workbook = openpyxl.load_workbook(file_path)

  # Get the sheet you want to access
  sheet = workbook['Sheet1']

  # Iterate over the columns in the sheet
  for i,col in enumerate(sheet.columns):
      # Find the column you want to access
      if i == 1:
          # Print the values in the column
          for cell in col:
            status = 'OFF'
            if str(cell.value) == 'true':
              status = 'ON '
            print('\n\n\n')
            print('------------------------------------')
            print(f"| Algorithm Activity Status  : {status} |")
            print('------------------------------------')
            print('\n\n\n')
            return cell.value







# def read_xlsx_file(directory = 'configuration' , filename = 'vehicles_generating.xlsx' , column = 'generating_number'):
#   file_path = f"{directory}/{filename}"
#   xlSheet = "Sheet1"
#   # Load the data from the xlsx file
#   df = pd.read_excel(file_path,sheet_name = xlSheet)
#   data = {}
#   # Iterate over the rows of the dataframe
#   for _, row in df.iterrows():
#       # Access data for each column by column name
#       vehicle_type = row['vehicle_type']
#       generating_number = row[column]
#       data[vehicle_type]=generating_number
#   return data
def read_xlsx_file(directory = 'configuration' , filename = 'vehicles_generating.xlsx' , column = 'generating_number'):
  file_path = f"{directory}/{filename}"
  xlSheet = "Sheet1"
  
  # Open the Excel file
  xlsx = pd.ExcelFile(file_path)
  
  # Check if the sheet name is valid
  if xlSheet not in xlsx.sheet_names:
    raise ValueError(f"Sheet '{xlSheet}' not found in file '{filename}'")
  
  # Load the data from the xlsx file
  df = pd.read_excel(xlsx, sheet_name=xlSheet)
  data = {}
  # Iterate over the rows of the dataframe
  for _, row in df.iterrows():
      # Access data for each column by column name
      vehicle_type = row['vehicle_type']
      generating_number = row[column]
      data[vehicle_type]=generating_number
  return data


# def read_xlsx_file(directory = 'configuration' , filename = 'vehicles_generating.xlsx'):
#   file_path = f"{directory}/{filename}"
#   xlSheet = "Sheet1"
#   # Load the data from the xlsx file
#   df = pd.read_excel(file_path,sheet_name = xlSheet)

#   # Iterate over the rows of the dataframe
#   for _, row in df.iterrows():
#       # Access data for each column by column name
#       vehicle_type = row['vehicle_type']
#       generating_number = row['generating_number']
#       GD.vehicles_generating[vehicle_type]=generating_number
      




def create_directory():
  current_time = get_current_time()
  path = f'output/{current_time}'
  os.makedirs(path, exist_ok=True)
  return path , current_time



def create_xlsx_file(path='temp'):
  # Create a new empty workbook
  wb = openpyxl.Workbook()
    
  # Get the active sheet
  sheet = wb.active
  print(sheet)
  # Modify the data in the sheet
  sheet['A1'] = 'vehicle_type'
  sheet['B1'] = 'vehicle_speed_avg'
  
  # Save the workbook to an xlsx file
  wb.save(f'{path}/vehicles_avg_speeds.xlsx')








def append_dict_to_xlsx( filename , data ,path='temp'):
  if(len(data) > 1):
    df = pd.read_excel(f"{path}/{filename}")

    # Append the new row to the dataframe
    df = df.append(data, ignore_index=True)

    # Write the data back to the xlsx file
    df.to_excel(f"{path}/{filename}", index=False)









def remove_directory(directory="output"):
  # Check if the directory exists
  if os.path.exists(directory):
      # Delete the directory and all of its contents
      shutil.rmtree(directory)
      print("Directory deleted")
  else:
      # Print an error message
      print("Directory does not exist")








def plot_vehicle_average_speed(path='temp'):

  file_path = f"{path}/vehicles_avg_speeds.xlsx"
  xlSheet = "Sheet1"
  # Open the Excel file
  xlsx = pd.ExcelFile(file_path)
  
     # Check if the sheet name is valid
  if xlSheet not in xlsx.sheet_names:
    raise ValueError(f"Sheet '{xlSheet}' not found in file '{file_path}'")
  # Load the data from the xlsx file
  df = pd.read_excel(file_path,sheet_name = xlSheet)
  
  colors = ['skyblue' , 'g' , 'r' , 'pink', 'coral']
  # Create a mapping from vehicle type to integer index
  vehicle_type_to_index = {'car': 0, 'bus': 1, 'truck': 2, 'motorcycle': 3}

  # Use the map method to transform the vehicle_type column
  df['vehicle_type_index'] = df['vehicle_type'].map(vehicle_type_to_index)
  if(len(sim.simulation) > 0):
  # Plot the scatter plot using the transformed column
    df.plot(kind="scatter", x="vehicle_type", y="vehicle_speed_avg", color=[colors[int(x)] for x in df['vehicle_type_index']])

  # Customize the appearance of the plot
  plt.xlabel("Vehicle Type")
  plt.ylabel("Average Speed (km/h)")
  plt.title("Average Speeds for Different Vehicle Types")

  plt.savefig(f"{path}/avg_speed_for_each_vehicle.png", dpi=300)




# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen.canvas import Canvas

# def plot_average_speeds_for_each_vehicle_type(path):
  
#     file_path = f"{path}/vehicle_data.xlsx"
#     xlSheet = "Sheet1"
#     # Load the data from the xlsx file
#     df = pd.read_excel(file_path,sheet_name = xlSheet)
    
#     # Create a scatter plot of the data
#     df.plot(kind="scatter",x="vehicle_type", y="vehicle_speed_avg")
    
#     # Group the rows by vehicle type and calculate the mean average speed
#     mean_speeds = df.groupby("vehicle_type").mean()
     
#     # # Create a bar plot of the mean average speeds
#     mean_speeds.plot(kind="bar")
  
#     # Customize the appearance of the plot
#     plt.xlabel("Vehicle Type")
#     plt.ylabel("Average Speed (km/h)")
#     plt.title("Mean Average Speeds for Different Vehicle Types")
    
#     # Save the plot to a file
#     plt.savefig("average_speeds_for_each_type.png", dpi=300)
    
#     # Create a new PDF document with a size of letter paper
#     pdf_file = f"{path}/report.pdf"
#     pdf_canvas = Canvas(pdf_file, pagesize=letter)
    
#     # Add the plot image to the PDF document
#     pdf_canvas.drawImage("average_speeds_for_each_type.png", x=100, y=500, width=400, height=300)
#     pdf_canvas.showPage()
#     # Save the PDF document
#     pdf_canvas.save()



def plot_average_speeds_for_each_vehicle_type(path='temp'):
  
    file_path = f"{path}/vehicles_avg_speeds.xlsx"
    xlSheet = "Sheet1"
    # Load the data from the xlsx file
    
     # Open the Excel file
    xlsx = pd.ExcelFile(file_path)
  
     # Check if the sheet name is valid
    if xlSheet not in xlsx.sheet_names:
      raise ValueError(f"Sheet '{xlSheet}' not found in file '{file_path}'")
    df = pd.read_excel(file_path,sheet_name = xlSheet)
    # Create a scatter plot of the data
    df.plot(kind="scatter",x="vehicle_type", y="vehicle_speed_avg")
    if(len(sim.simulation)>0):
    # Group the rows by vehicle type and calculate the mean average speed
      mean_speeds = df.groupby("vehicle_type").mean()
     
    # # Create a bar plot of the mean average speeds
      mean_speeds.plot(kind="bar", cmap='viridis')

    
    # Get the x-coordinates of the bar plot
      x_coords = list(range(len(mean_speeds)))
    
      for i, (index, row) in enumerate(mean_speeds.iterrows()):
        plt.text(x_coords[i]-0.25, row["vehicle_speed_avg"]+0.5, f"{row['vehicle_speed_avg']:.1f}", fontsize=10, ha="center")

    # Customize the appearance of the plot
    plt.xlabel("Vehicle Type")
    plt.ylabel("Average Speed (km/h)")
    plt.title("Mean Average Speeds for Different Vehicle Types")
    
    plt.savefig(f"{path}/average_speeds_for_each_type.png", dpi=300)

