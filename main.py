# Library imports
import RPi.GPIO as GPIO
import board
import busio
from flask import Flask, render_template, request, jsonify
import adafruit_sht4x
import adafruit_seesaw.seesaw as ss
import smbus2
import json

#disable gpio warings 
GPIO.setwarnings(False)

# Set up the GPIO pins for the relay
GPIO.setmode(GPIO.BCM)

pinList = [17, 22, 27, 10]

for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

# Sensor setup
i2c = busio.I2C(3, 2)
sht = adafruit_sht4x.SHT4x(i2c, address=0x44)
ss = ss.Seesaw(i2c, addr=0x36)

# Define a class for relay control
# class Relay:
#     def __init__(self, pin):
#         self.pin = pin
#         GPIO.setup(self.pin, GPIO.OUT)
#         GPIO.output(self.pin, GPIO.LOW)

#     def on(self):
#         GPIO.output(self.pin, GPIO.HIGH)

#     def off(self):
#         GPIO.output(self.pin, GPIO.LOW)

#     def is_on(self):
#         return GPIO.input(self.pin) == GPIO.HIGH

#     def is_off(self):
#         return GPIO.input(self.pin) == GPIO.LOW

# Define the set_relay function
# def set_relay(channel, state):
#     relay = Relay(channel)
#     if state == "on":
#         relay.on()
#     else:
#         relay.off()

# Set up the Flask app
app = Flask(__name__, static_folder='static')

# def light1():
#     GPIO.output(17, GPIO.LOW)    

def read_sensor_data():
    # Read temperature in Celsius
    temperature_c = sht.temperature
    # Convert temperature from Celsius to Fahrenheit
    temperature_f = temperature_c * 1.8 + 32
    humidity = sht.relative_humidity
    moisture = ss.moisture_read()

    return {
        'temperature': temperature_f,
        'humidity': humidity,
        'moisture': moisture
    }

# Define routes for the web server
@app.route("/")
def index():
    data = read_sensor_data()
    # Open a file for writing
    with open("static/data.json", "w") as f:
        # Write data to the file
        json.dump(data, f)
    return render_template("index.html")

@app.route('/set-relay', methods=['POST'])
def set_relay_route():
    channel = request.json.get('channel')
    state = request.json.get('state')
    
    # Use the set_relay function to control the relay
    if state == "on":
        GPIO.output(channel, GPIO.LOW)
    else:
        GPIO.output(channel, GPIO.HIGH)

    # Return a response indicating success
    return jsonify({'success': True})


@app.route("/sensor_data")
def sensor_data():
    data = read_sensor_data()
    jsonSensorData = jsonify(data)
    return jsonSensorData

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
