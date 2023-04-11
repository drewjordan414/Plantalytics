import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
import board
import busio
import adafruit_tsl2591
import adafruit_sht4x
import adafruit_seesaw
import adafruit_seesaw.seesaw as seesaw
from sensor_data import capture_sensor_data
from model import make_decisions
from model import plant_classification_model, plant_disease_detection_model, environment_optimization_model

# Define the sensor i2c data
tsl_address = 0x29
sht_address = 0x44
stemma_address = 0x36

# Initialize the i2c bus
try:
    i2c = busio.I2C(board.SCL, board.SDA)
except OSError:
    connected = False
    tsl_sensor = None
    sht_sensor = None
    stemma_sensor = None
else:
    connected = True
    # Initialize the sensors
    tsl_sensor = adafruit_tsl2591.TSL2591(i2c)
    sht_sensor = adafruit_sht4x.SHT4x(i2c)
    stemma_sensor = seesaw.Seesaw(i2c, addr=stemma_address)

def capture_sensor_data():
    if connected:
        lux = tsl_sensor.lux
        temperature = sht_sensor.temperature
        temperature_f = temperature * 9/5 + 32  # Convert temperature to Fahrenheit
        humidity = sht_sensor.relative_humidity
        # Read data from STEMMA soil sensor
        moisture = stemma_sensor.moisture_read()
        return {'temperature': temperature_f, 'humidity': humidity, 'moisture': moisture, 'light_intensity': lux}
    else:
        # Return a message indicating that the sensors are not connected
        return {'message': 'Sensors not connected'}

class PlantMonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 480)
        self.setWindowTitle('Plant Monitor')

        vbox = QVBoxLayout()

        sensor_data = capture_sensor_data()

        if 'message' in sensor_data:
            # Display a message indicating that the sensors are not connected
            message_label = QLabel(sensor_data['message'])
            vbox.addWidget(message_label)
        else:
            texts = [
                f"Temperature: {sensor_data['temperature']:.1f}F",  # Display temperature in Fahrenheit
                f"Humidity: {sensor_data['humidity']:.1f}%",
                f"Moisture: {sensor_data['moisture']:.1f}%",
                f"Light Intensity: {sensor_data['light_intensity']:.1f} lux",
            ]

            for text in texts:
                label = QLabel(text)
                vbox.addWidget(label)

        self.setLayout(vbox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    plant_monitor = PlantMonitor()
    plant_monitor.show()
    sys.exit(app.exec_())

