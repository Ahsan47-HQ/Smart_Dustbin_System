**Smart Dustbin System**

This system detects and classifies waste at collection point into different categories and places them in the correct compartment using YOLO, EfficientNet, and Sensor Fusion.

**Architecture**:
--> Object Detection: YOLOv8n
--> Image Classification: EfficientNetV2B0
--> Sensors used: DHT11 temperature/humidity sensor, HC-SR04 ultrasonic sensor
--> Control unit: Raspberry Pi 5 - 4GB RAM variant