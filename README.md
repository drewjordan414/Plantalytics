# Plantalytics

## About
Plantalytics is a smart plant monitor that uses sensors to track environmental conditions, such as temperature, humidity, and soil moisture. It leverages machine learning models to optimize plant growth, diagnose diseases, and make decisions on plant care. The data is displayed on an LCD and a GUI.

## Parts List
- Raspberry Pi (3B, 3B+, 4, or Zero W) - The main controller for the project.
- Micro SD Card (at least 8GB) - For Raspberry Pi's operating system and storage.
- Power supply for Raspberry Pi - To provide power for the Raspberry Pi.
- TSL2591 Light Sensor - To measure light intensity.
- SHT40 Temperature and Humidity Sensor - To measure temperature and humidity.
- Adafruit STEMMA Soil Sensor - To measure soil moisture levels.
- 5" touch screen for Raspberry Pi
- Breadboard - For assembling the circuitry.
- Jumper wires - For connecting sensors and other components to the Raspberry Pi.
- I2C Interface - To connect multiple I2C devices (sensors) to the Raspberry Pi.
- Optional: Actuators (water pump, fans, etc.) - For automating tasks based on the decisions made by the program.

In addition to the hardware components, you will need the following software and libraries:
- Raspberry Pi OS - The operating system for the Raspberry Pi.
- Python - The programming language used for writing the project's code.
- TensorFlow - A machine learning library for loading and using the trained models.
- Adafruit CircuitPython libraries - For interfacing with the sensors (TSL2591, SHT40, and STEMMA Soil Sensor).
- Tkinter - A Python library for creating the graphical user interface.
- NumPy - A library for numerical operations in Python.
- Pandas - A library for data manipulation and analysis in Python.

## About the Models
1. **plant_classification_model**: This model is a trained machine learning model responsible for classifying plants based on their features. Given input data (such as images or sensor data), it predicts the type or species of the plant. The model is stored in the 'plant_classification_model.h5' file and loaded into the program using TensorFlow.

2. **plant_disease_detection_model**: This model is designed to detect plant diseases based on input data (typically images of plant leaves or other plant parts). The model identifies whether a plant is healthy or suffering from a specific disease. It is stored in the 'plant_disease_detection_model.h5' file and loaded into the program using TensorFlow.

3. **environment_optimization_model**: This model takes environmental data (such as temperature, humidity, and moisture) as input and predicts the optimal growing environment for a plant. It helps in adjusting the environment to promote healthy growth or mitigate issues related to suboptimal conditions. The model is stored in the 'environment_optimization_model.h5' file and loaded into the program using TensorFlow.

