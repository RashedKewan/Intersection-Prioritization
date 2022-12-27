import csv
import os
import shutil
import matplotlib.pyplot as plt
import pandas as pd
import GlobalData as GD
import openpyxl


def read_xlsx_file(directory = 'configuration' , filename = 'vehicles_generating.xlsx'):
  file_path = f"{directory}/{filename}"
  xlSheet = "Sheet1"
  # Load the data from the xlsx file
  df = pd.read_excel(file_path,sheet_name = xlSheet)

  # Iterate over the rows of the dataframe
  for _, row in df.iterrows():
      # Access data for each column by column name
      vehicle_type = row['vehicle_type']
      generating_number = row['generating_number']
      GD.vehicles_generating[vehicle_type]=generating_number
      

def create_xlsx_file():
  # Open the file in append mode
  if not os.path.exists('output'):
    os.mkdir('output')
  # Create a new empty workbook
  wb = openpyxl.Workbook()
    
  # Get the active sheet
  sheet = wb.active

  # Modify the data in the sheet
  sheet['A1'] = 'vehicle_type'
  sheet['B1'] = 'vehicle_speed_avg'
  
  # Save the workbook to an xlsx file
  wb.save('output/vehicle_data.xlsx')



def append_dict_to_xlsx( filename , data , directory="output" , fieldnames=['vehicle_type', 'vehicle_speed_avg']):
  # Open the file in append mode
  if not os.path.exists(directory):
    os.mkdir('output')
  df = pd.read_excel(f"{directory}/{filename}")

  # Append the new row to the dataframe
  df = df.append(data, ignore_index=True)

  # Write the data back to the xlsx file
  df.to_excel(f"{directory}/{filename}", index=False)





def remove_directory(directory="output"):
  # Check if the directory exists
  if os.path.exists(directory):
      # Delete the directory and all of its contents
      shutil.rmtree(directory)
      print("Directory deleted")
  else:
      # Print an error message
      print("Directory does not exist")




def plot_vehicle_average_speed(directory="output" , filename="vehicle_data.xlsx"):
  if not os.path.exists(directory):
    os.mkdir('output')

  file_path = f"{directory}/{filename}"
  xlSheet = "Sheet1"
  # Load the data from the xlsx file
  df = pd.read_excel(file_path,sheet_name = xlSheet)
  
  # # Create a scatter plot of the data
  # df.plot(kind="scatter", x="vehicle_type", y="vehicle_speed_avg")


  colors = ['red', 'blue', 'green', 'orange']
  # Create a mapping from vehicle type to integer index
  vehicle_type_to_index = {'car': 0, 'truck': 1, 'motorcycle': 2, 'bus': 3}

  # Use the map method to transform the vehicle_type column
  df['vehicle_type_index'] = df['vehicle_type'].map(vehicle_type_to_index)

  # Plot the scatter plot using the transformed column
  df.plot(kind="scatter", x="vehicle_type", y="vehicle_speed_avg", color=[colors[int(x)] for x in df['vehicle_type_index']])



  # Customize the appearance of the plot
  plt.xlabel("Vehicle Type")
  plt.ylabel("Average Speed (km/h)")
  plt.title("Average Speeds for Different Vehicle Types")

  plt.savefig(f"{directory}/avg_speed_for_each_vehicle.png", dpi=300)




def plot_average_speeds_for_each_vehicle_type(directory="output", filename="vehicle_data.xlsx"):
    if not os.path.exists(directory):
      os.mkdir('output')

    file_path = f"{directory}/{filename}"
    xlSheet = "Sheet1"
    # Load the data from the xlsx file
    df = pd.read_excel(file_path,sheet_name = xlSheet)
    
    # Create a scatter plot of the data
    df.plot(kind="scatter", x="vehicle_type", y="vehicle_speed_avg")

    # Group the rows by vehicle type and calculate the mean average speed
    mean_speeds = df.groupby("vehicle_type").mean()

    # # Create a bar plot of the mean average speeds
    mean_speeds.plot(kind="bar")

    # Customize the appearance of the plot
    plt.xlabel("Vehicle Type")
    plt.ylabel("Average Speed (km/h)")
    plt.title("Mean Average Speeds for Different Vehicle Types")
    
    plt.savefig(f"{directory}/average_speeds_for_each_type.png", dpi=300)
