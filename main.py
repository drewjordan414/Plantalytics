# Library imports
import RPi.GPIO as GPIO
import time
import datetime
import os
import sys
import adafruit_sht4x
import adafruit_seesaw.seesaw as ss
import board
import busio
from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
import cv2
import torch
import torchvision.models as models
import numpy as np

# Set up the GPIO pins for the relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

# Sensor setup
i2c = board.I2C()
i2c_bus = busio.I2C(board.SCL, board.SDA)
sht = adafruit_sht4x.SHT4x(i2c_bus)
ss = ss.Seesaw(i2c_bus, addr=0x36)

# Define a class for relay control
class Relay:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def is_on(self):
        return GPIO.input(self.pin) == GPIO.HIGH

    def is_off(self):
        return GPIO.input(self.pin) == GPIO.LOW

# Define the set_relay function
def set_relay(channel, state):
    relay = Relay(channel)
    if state == "on":
        relay.on()
    elif state == "off":
        relay.off()

# Set up the Flask app
app = Flask(__name__)

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

# Define the route for plant disease detection
@app.route("/plant_disease_detection")
def plant_disease_detection():
    # Load the trained model
    model1 = models.resnet18(pretrained=False)
    num_ftrs = model1.fc.in_features
    model1.fc = torch.nn.Linear(num_ftrs, 38)
    model1.load_state_dict(torch.load('plant-disease-model-complete.pth'))

    model2 = models.resnet18(pretrained=False)
    num_ftrs = model2.fc.in_features
    model2.fc = torch.nn.Linear(num_ftrs, 38)
    model2.load_state_dict(torch.load('plant-disease-model.pth'))

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model1.to(device)
    model2.to(device)

    # Capture a frame from the Raspberry Pi camera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame = cv2.resize(frame, (224, 224))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = frame.transpose((2, 0, 1))
    frame = frame/255.0

    # Perform the detection
    model1.eval()
    model2.eval()
    with torch.no_grad():
        input = torch.from_numpy(frame).unsqueeze(0).float().to(device)
        output1 = model1(input)
        output2 = model2(input)
        _, preds1 = torch.max(output1, 1)
        _, preds2 = torch.max(output2, 1)
        pred = preds1.item() if preds1.item() == preds2.item() else 38

    # Return the result to the user interface
    if pred == 0:
        result = "Healthy Plant"
    else:
        result = "Diseased Plant"
    return render_template("page2.html", result=result)

# Define routes for the web server
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/set_relay", methods=["POST"])
def set_relay_route():
    channel = int(request.form["channel"])
    state = request.form["state"]
    set_relay(channel, state)
    return "OK"

def gen():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/sensor_data")
def sensor_data():
    data = read_sensor_data()
    return jsonify(data)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


