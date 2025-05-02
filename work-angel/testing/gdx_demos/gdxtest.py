import os
import csv
import time

import numpy as np
import matplotlib.pyplot as plt

from gdx import gdx
gdx = gdx.gdx()

## Application Intro
intro_message = "This is a working demo for godirect sensor data collection.\n"
print(intro_message)

## Styling Options:
styles = {
    '1': 'ggplot',
    '2': 'dark_background'
}

style_msg = "Please select a number for a pyplot style: \n(1) ggplot \n(2) dark_background\n\n Input number: "
style_input = str(input(style_msg))

print(style_msg)
plt.style.use(styles[style_input])
if style_input == '2':
    plt.grid(alpha=0.5)

## File name setting
file_msg = "Enter a file name for the .csv file you are creating. For example, 'file_name.csv' without the apostrophes. \n If no file name is entered, the file will be named 'my_data.csv' \n\nEnter file name here: "
filename = input(file_msg)
if len(filename) < 3:
    filename = 'my_data.csv'
if filename[-4:] != ".csv":
    filename = filename + ".csv"

print(f' Your file name is: "{filename}".')

## Initial Sensor Configuration:
gdx.open(connection='usb') # Open Go Direct sensor through USB.
gdx.select_sensors() # Asks for which sensor will be used from the connected devices. 
#For the motion sensor, the options are 5, 6, 7, and they are all mutually exclusive.'''

# This gets the name and units of the sensors selected. gdx
column_headers = gdx.enabled_sensor_info() 

# Store the number of sensors. This variable is used in plot_graph() and print_table() gdx
#number_of_sensors=len(column_headers)

#print(column_headers)

## Data Acquisition Configuration:
# Plot Initialization
fig, ax = plt.subplots()


# Configuration Parameters
def config():
    frequency = 20 #Hz
    collection_time = round(float(input('Enter collection time in seconds (multiples of 0.1): ')), 1)
    print(f'collection time: {collection_time} s\n')
    collection_time_ms = collection_time * 1000 #ms
    number_of_readings = collection_time * frequency
    time_between_readings_in_seconds = 0.05
    return collection_time_ms, number_of_readings, time_between_readings_in_seconds

period_in_ms, number_of_readings, time_between_readings_in_seconds = config()

def plot_graph(sensor_times, sensor_readings0):
    
    # Customize the graph See Pyplot documentation
    ax.scatter(sensor_times,sensor_readings0, color='r',label=column_headers[0]) #red line for sensor 1

    plt.ylabel('Position(m)')
    plt.xlabel('Time(s)')
    plt.grid(True) #This controls whether there is a grid on the graph
    plt.pause (0.05) # display the graph briefly, as the readings are taken

def print_table():
    print ("Data Table:")
    print ('Time (s) ', 'Position (m)') #label the data table that will be printed on the Python Shell

    # The print_table_string is a list of strings. Each element in the list contains the time and readings.
    # This variable is created in the Data Collection loop.
    for string in print_table_string:
        print(string)

# Data Collection:
def data_collect():
    collection_complete=False
    while not collection_complete:
        try:
            time = 0
            print ('Collecting Data...')
            
            #Start data collection at the specified rate. The period argument is in milliseconds
            gdx.start(period_in_ms) 

            # Variables to store the time and readings from the sensors
            sensor_times=[]
            sensor_readings0=[]
            print_table_string = []

            # Print the column headers, starting with Time(s)
            column_headers = 'Time(s), ' + 'Position(m)'
            print(column_headers)
            

            for i in range(0,int(number_of_readings)):
                
                # Create a list of times to be used in the graph and data table.
                sensor_times.append(time)

                # This is where we are reading the list of measurements from the sensors.
                measurements=gdx.read() 
                if measurements == None: 
                    break 

                # Store each sensor's measurement in a list to be used in plot_graph() and print_table()
                data_string = ''
                title_string =''
                for data in measurements:
                    sensor_readings0.append(data)
                    
                    # Build a string for printing to the terminal and to be used as the title of the graph
                    round_data = str(round(data,2))
                    data_string = data_string + round_data + '   '
                    title_string = title_string + round_data + '(m)' + '   '
                    
                    # Write row for .csv document
                    #csv_writer.writerow(str(time) + ',' + str(measurements))

                # Create a list for the print_table() function. Only used for fast data collection
                if time_between_readings_in_seconds<=0.04: #originally 0.4
                    print_table_string.append(str(round(time,2)) + '   ' + data_string)

                # For slower data collection, print the data to the terminal and the graph
                if  time_between_readings_in_seconds>0.04:

                    # Print the time and the data to the terminal
                    print(str(round(time,2)) + '   '+ data_string)

                    # If the last reading is finished update the graph's title
                    if  i >=number_of_readings-1: 
                        plt.title(column_headers_string +' vs '+'Time (s)')
                    
                    # If collection is in process, use the data as the graph's title, for real-time updates
                    else:
                        plt.title(title_string)
                    
                    # Call the plot_graph() function to update the graph with the new data set. 
                    plot_graph(sensor_times[-1], sensor_readings0[-1]) 

                # Update the time variable with the new time for the next data point
                time = time+time_between_readings_in_seconds 

            # The data collection loop is finished
            collection_complete=True
            print ('data  collection complete')
            print ('Number of readings: ',i+1)
            print ('Time between readings: ',time_between_readings_in_seconds, " s")
            print ('Total time for data collection ', time, ' s')
            
            # Stop sensor readings and disconnect the device.
            gdx.stop()
            gdx.close()
            
            # For fast collection we did not print to the graph during data collection. Now that all data
            # have been collected, send the data to the print_table() and plot_graph() function.
            if  time_between_readings_in_seconds<=0.04:
                print_table()
                plt.title(column_headers[0]+' vs '+'Time (s)') #put a title on the top of graph
                plot_graph()
            

        except KeyboardInterrupt:
            collection_complete=True
            gdx.stop() #Stop sensor readings
            gdx.close()#Disconnect the device
            print ('data  collection stopped by keypress')
            print ('Number of readings: ',i+1)

    # Command to leave the graph window open when the program ends.
    plt.show()

data_collect()