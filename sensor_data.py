#code for the sensors and data collection from the sensors
import time
import board
import busio
import adafruit_tsl2591
import adafruit_sht4x
import adafruit_seesaw
import adafruit_seesaw.seesaw as seesaw

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize TSL2591 light sensor
tsl = adafruit_tsl2591.TSL2591(i2c)

# Initialize SHT40 temperature and humidity sensor
sht = adafruit_sht4x.SHT4x(i2c)

# Initialize STEMMA soil sensor
ss = SeesawSoil(i2c, addr=0x36)

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
