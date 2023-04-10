import time
import board
import busio 
import adafruit_tsl2591
import adafruit_sht4x
import adafruit_seesaw
from adafruit_seesaw import SeesawSoil
import numpy as np 
import pandas as pd 
import tensorflow as tf 
import digitalio
import adafruit_character_lcd.character_lcd as charlcd
import tkinter as tk 

# Initialize the Tkinter window
window = tk.Tk()
window.title("Plant Monitor")
window.geometry("400x200")

# Define meters on the GUI
moisture_meter = tk.Label(window, text="Moisture: ")
moisture_meter.pack()

temperature_meter = tk.Label(window, text="Temperature: ")
temperature_meter.pack()

humidity_meter = tk.Label(window, text="Humidity: ")
humidity_meter.pack()

# Load the trained machine learning models
plant_classification_model = tf.keras.models.load_model('plant_classification_model.h5')
plant_disease_detection_model = tf.keras.models.load_model('plant_disease_detection_model.h5')
environment_optimization_model = tf.keras.models.load_model('environment_optimization_model.h5')

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize TSL2591 light sensor
tsl = adafruit_tsl2591.TSL2591(i2c)

# Initialize SHT40 temperature and humidity sensor
sht = adafruit_sht4x.SHT4x(i2c)

# Initialize STEMMA soil sensor
ss = SeesawSoil(i2c, addr=0x36)

# Initialize LCD display
lcd_columns = 16
lcd_rows = 2
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D26)
lcd_d5 = digitalio.DigitalInOut(board.D19)
lcd_d6 = digitalio.DigitalInOut(board.D13)
lcd_d7 = digitalio.DigitalInOut(board.D6)
lcd_backlight = digitalio.DigitalInOut(board.D5)

lcd = charlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

def capture_sensor_data():
    # Read data from TSL2591 light sensor
    lux = tsl.lux

    # Read data from SHT40 temperature and humidity sensor
    temperature = sht.temperature
    humidity = sht.relative_humidity

    # Read data from STEMMA soil sensor
    moisture = ss.moisture_read()

    # Display sensor data on LCD
    lcd.clear()
    lcd.message('Temp: {:.1f} C\n'.format(temperature))
    lcd.message('Humidity: {:.1f} %'.format(humidity))

    # Return sensor data as a dictionary
    return {'temperature': temperature, 'humidity': humidity, 'moisture': moisture}
# Define a function to update the meters on the GUI
def update_meters():
    # Read data from STEMMA soil sensor
    moisture = ss.moisture_read()
    # Read data from SHT40 temperature and humidity sensor
    temperature = sht.temperature
    humidity = sht.relative_humidity
    # Update meters on the GUI
    moisture_meter.config(text="Moisture: {:.1f}%".format(moisture))
    temperature_meter.config(text="Temperature: {:.1f}C".format(temperature))
    humidity_meter.config(text="Humidity: {:.1f}%".format(humidity))
    # Call this function again after 5 seconds
    window.after(5000, update_meters)

# Define a function to make decisions based on the outputs of the models
def make_decisions(environment_prediction, sensor_data):
    # Make decisions based on plant health and environment factors
    if environment_prediction >= 0.75:
        decision = 'continue'
    elif environment_prediction >= 0.5:
        decision = 'treat'
    else:
        decision = 'replace'
    
    # Return decision
    return decision

# Define a function to control the actuators based on the decisions
def control_actuators(decision):
    # Control actuators based on decision
    if decision == 'continue':
        # Your code here for continuing plant growth
        pass
    elif decision == 'treat':
        # Your code here for treating plant disease
        pass
    elif decision == 'replace':
        # Your code here for replacing the plant
        pass

# Define a function for the main loop
def main_loop():
    # Capture sensor data and predict optimal environment
    sensor_data = capture_sensor_data()
    sensor_data_array = np.array([[sensor_data['temperature'], sensor_data['humidity'], sensor_data['moisture']]])
    environment_prediction = environment_optimization_model.predict(sensor_data_array)
    
    # Make decisions based on predictions
    decision = make_decisions(environment_prediction, sensor_data)
    
    # Control actuators based on decisions
    control_actuators(decision)
    
    # Call this function again after 5 seconds
    window.after(5000, main_loop)

# Start updating meters on the GUI
update_meters()

# Start the main loop
main_loop()

# Start the Tkinter main event loop
window.mainloop()
