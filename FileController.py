import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import GlobalData as GD


def create_csv_file(filename, fieldnames=['vehicle_type', 'vehicle_speed_avg']):
  # Open the file in write mode
  with open(filename, 'w', newline='') as f:
    # Create a writer object
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()



def append_dict_to_csv(filename, data , fieldnames=['vehicle_type', 'vehicle_speed_avg']):
  # Open the file in append mode
  with open(filename, 'a', newline='') as f:
    # Create a writer object
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    # Write the header if the file is empty
    if f.tell() == 0:
      writer.writeheader()
      
    # Write the data as a new row
    writer.writerow(data)


def remove_file(filename):
# Check if the file exists
    if os.path.exists(filename):
        # Delete the file
        os.remove(filename)
        print("File deleted")
    else:
        # Print an error message
        print("File does not exist")


def plot_vehicle_average_speed():
  # Load the data into a DataFrame
  df = pd.read_csv("vehicle_data.csv", usecols=["vehicle_type", "vehicle_speed_avg"])

  # Create a scatter plot of the data
  df.plot(kind="scatter", x="vehicle_type", y="vehicle_speed_avg")

  # Customize the appearance of the plot
  plt.xlabel("Vehicle Type")
  plt.ylabel("Average Speed (km/h)")
  plt.title("Average Speeds for Different Vehicle Types")

  plt.savefig("avg_speed_for_each_vehicle.png", dpi=300)




def plot_average_speeds():
    # Load the data into a DataFrame
    df = pd.read_csv("vehicle_data.csv", usecols=["vehicle_type", "vehicle_speed_avg"])

    # Group the rows by vehicle type and calculate the mean average speed
    mean_speeds = df.groupby("vehicle_type").mean()

    # Create a bar plot of the mean average speeds
    mean_speeds.plot(kind="bar")

    # Customize the appearance of the plot
    plt.xlabel("Vehicle Type")
    plt.ylabel("Average Speed (km/h)")
    plt.title("Mean Average Speeds for Different Vehicle Types")
    
    plt.savefig("average_speeds_for_each_type.png", dpi=300)


