# Plantalytics
About Plantalytics is a smart plant monitor that uses sensors to track environmental conditions, such as temperature, humidity, and soil moisture. It leverages machine learning models to optimize plant growth, diagnose diseases, and make decisions on plant care. The data is displayed on an LCD and a GUI.

# About the Models
1) plant_classification_model: This model is a trained machine learning model responsible for classifying plants based on their features. Given input data (such as images or sensor data), it predicts the type or species of the plant. The model is stored in the 'plant_classification_model.h5' file and loaded into the program using TensorFlow.

2) plant_disease_detection_model: This model is designed to detect plant diseases based on input data (typically images of plant leaves or other plant parts). The model identifies whether a plant is healthy or suffering from a specific disease. It is stored in the 'plant_disease_detection_model.h5' file and loaded into the program using TensorFlow.

3) environment_optimization_model: This model takes environmental data (such as temperature, humidity, and moisture) as input and predicts the optimal growing environment for a plant. It helps in adjusting the environment to promote healthy growth or mitigate issues related to suboptimal conditions. The model is stored in the 'environment_optimization_model.h5' file and loaded into the program using TensorFlow.
