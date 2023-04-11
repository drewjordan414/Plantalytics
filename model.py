#code for loading the models and decision making based on sensor data 
import numpy as np
import tensorflow as tf
from sensor_data import capture_sensor_data
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT)  # Lights
GPIO.setup(15, GPIO.OUT)  # Fan
GPIO.setup(18, GPIO.OUT)  # Water

# Load the trained machine learning models
plant_classification_model = tf.keras.models.load_model('plant_classification_model.h5')
plant_disease_detection_model = tf.keras.models.load_model('plant_disease_detection_model.h5')
environment_optimization_model = tf.keras.models.load_model('environment_optimization_model.h5')

# Define a function to make decisions based on the outputs of the models
def make_decisions():
    sensor_data = capture_sensor_data()
    sensor_data_array = np.array([[sensor_data['temperature'], sensor_data['humidity'], sensor_data['moisture']]])

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
        # Turn on lights and fan, and water plant
        GPIO.output(14, GPIO.HIGH)  # Turn on lights
        GPIO.output(15, GPIO.HIGH)  # Turn on fan
        GPIO.output(18, GPIO.HIGH)  # Water plant
    elif decision == 'treat':
        # Turn off lights and fan, and do not water plant
        GPIO.output(14, GPIO.LOW)  # Turn off lights
        GPIO.output(15, GPIO.LOW)  # Turn off fan
        GPIO.output(18, GPIO.LOW)  # Do not water plant
