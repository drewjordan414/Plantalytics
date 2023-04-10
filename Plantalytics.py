import time
import board
import busio
import adafruit_tsl2591
import adafruit_sht4x
import adafruit_seesaw
from adafruit_seesaw import SeesawSoil
import numpy as np
import tensorflow as tf
import pygame

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize TSL2591 light sensor
tsl = adafruit_tsl2591.TSL2591(i2c)

# Initialize SHT40 temperature and humidity sensor
sht = adafruit_sht4x.SHT4x(i2c)

# Initialize STEMMA soil sensor
ss = SeesawSoil(i2c, addr=0x36)

# Load the trained machine learning models
plant_classification_model = tf.keras.models.load_model('plant_classification_model.h5')
plant_disease_detection_model = tf.keras.models.load_model('plant_disease_detection_model.h5')
environment_optimization_model = tf.keras.models.load_model('environment_optimization_model.h5')

# Initialize the Pygame screen
pygame.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("Plant Monitor")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def capture_sensor_data():
    # Read data from TSL2591 light sensor
    lux = tsl.lux

    # Read data from SHT40 temperature and humidity sensor
    temperature = sht.temperature
    temperature_f = temperature * 9/5 + 32  # Convert temperature to Fahrenheit
    humidity = sht.relative_humidity

    # Read data from STEMMA soil sensor
    moisture = ss.moisture_read()

    # Return sensor data as a dictionary
    return {'temperature': temperature_f, 'humidity': humidity, 'moisture': moisture, 'light_intensity': lux}

# Define a function to make decisions based on the outputs of the models
def make_decisions(sensor_data_array):
    environment_prediction = environment_optimization_model.predict(sensor_data_array)

    if environment_prediction >= 0.75:
        decision = 'continue'
    elif environment_prediction >= 0.5:
        decision = 'treat'
    else:
        decision = 'unknown'
    
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

def update_display():
    screen.fill((0, 0, 0))

    sensor_data = capture_sensor_data()

    texts = [
        f"Temperature: {sensor_data['temperature']:.1f}F",  # Display temperature in Fahrenheit
        f"Humidity: {sensor_data['humidity']:.1f}%",
        f"Moisture: {sensor_data['moisture']:.1f}%",
        f"Light Intensity: {sensor_data['light_intensity']:.1f} lux",
    ]

    for i, text in enumerate(texts):
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (20, 20 + i * 40))

    pygame.display.flip()


def main_loop():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Capture sensor data and predict optimal environment
        sensor_data = capture_sensor_data()
        sensor_data_array = np.array([[sensor_data['temperature'], sensor_data['humidity'], sensor_data['moisture']]])
        
        # Make decisions based on predictions
        decision = make_decisions(sensor_data_array)
        
        # Control actuators based on decisions
        control_actuators(decision)

        update_display()
        time.sleep(5)

    pygame.quit()

main_loop()
