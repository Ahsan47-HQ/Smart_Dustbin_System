# Smart Dustbin System

An intelligent waste management system designed to automatically detect, classify, and segregate waste at the source using computer vision and sensor fusion.

---

## Overview

The Smart Dustbin System leverages deep learning models and real-time sensor data to identify different types of waste and direct them into appropriate compartments. This reduces manual effort, improves recycling efficiency, and supports sustainable waste management.

---

## System Architecture

### Object Detection
- Model: YOLOv8n  
- Detects waste objects in real time

### Image Classification
- Model: EfficientNetV2B0  
- Classifies detected waste into predefined categories

### Sensor Fusion
- DHT11: Temperature and humidity sensing  
- HC-SR04: Object proximity detection  

### Control Unit
- Raspberry Pi 5 (4GB RAM)  
- Handles inference, sensor input, and control logic  

---

## Waste Categories

- Plastic & Paper  
- Organic Waste  
- Glass & Light Bulbs  
- E-Waste, Metal & Batteries  

---

## Workflow

1. Ultrasonic sensor detects object presence  
2. Camera captures image  
3. YOLOv8 detects object region  
4. EfficientNet classifies waste type  
5. Sensor data refines decision  
6. Waste is directed into correct compartment  

---

## Features

- Real-time detection and classification  
- Multi-model pipeline (Detection + Classification)  
- Sensor-driven automation  
- Scalable for smart city deployment  
- Reduces manual sorting effort  

---

## Tech Stack

- Python  
- YOLOv8 (Ultralytics)  
- TensorFlow / Keras (EfficientNetV2B0)  
- Raspberry Pi OS  
- DHT11 Sensor  
- HC-SR04 Ultrasonic Sensor  

---

## Future Work

- IoT dashboard integration  
- Mobile app for analytics  
- Improved accuracy with larger datasets  
- Smart bin-level monitoring and alerts  

---

## Applications

- Smart cities  
- Public waste management  
- Residential complexes  
- Industrial waste segregation  

---

## Project Goal

To build a scalable and intelligent waste segregation system that integrates AI with real-world environmental sustainability.
