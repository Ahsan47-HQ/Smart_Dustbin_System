import socket
import pickle
import struct
import time
from picamera2 import Picamera2
from gpiozero import OutputDevice, InputDevice

# ULTRASONIC
TRIG = OutputDevice(5)
ECHO = InputDevice(6)

def get_distance():
    TRIG.off()
    time.sleep(0.05)

    TRIG.on()
    time.sleep(0.00001)
    TRIG.off()

    timeout = time.time() + 0.02

    while ECHO.value == 0:
        pulse_start = time.time()
        if time.time() > timeout:
            return None

    while ECHO.value == 1:
        pulse_end = time.time()
        if time.time() > timeout:
            return None

    duration = pulse_end - pulse_start
    return duration * 17150

def object_detected():
    count = 0
    for _ in range(5):
        d = get_distance()
        if d and d < 12:
            count += 1
        time.sleep(0.1)
    return count >= 3

# CAMERA
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()

# NETWORK
LAPTOP_IP = "192.168.137.1"   # CHANGE
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((LAPTOP_IP, PORT))

print("System ready...")

while True:
    if object_detected():
        print("Object detected → streaming")

        frame = picam2.capture_array()

        data = pickle.dumps(frame)
        message = struct.pack("Q", len(data)) + data
        client.sendall(message)

    else:
        print("Waiting...")
        time.sleep(0.5)