import socket
from gpiozero import OutputDevice
from time import sleep
import os

# FIX for Pi 5 GPIO
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

# ---------------- SENSOR ----------------
import board
import adafruit_dht

dht = adafruit_dht.DHT11(board.D4)

# ---------------- NETWORK ----------------
HOST = '0.0.0.0'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for laptop...")
conn, addr = server.accept()
print("Connected:", addr)

# ---------------- MOTOR ----------------
IN1 = OutputDevice(17)
IN2 = OutputDevice(27)
IN3 = OutputDevice(22)
IN4 = OutputDevice(23)

sequence = [
    (1,0,1,0),
    (0,1,1,0),
    (0,1,0,1),
    (1,0,0,1)
]

def step_motor(steps, direction=1, delay=0.005):
    seq = sequence if direction == 1 else sequence[::-1]
    for _ in range(steps):
        for step in seq:
            IN1.value, IN2.value, IN3.value, IN4.value = step
            sleep(delay)

def move_to_bin(bin_number):
    steps = bin_number * 13
    print(f"Bin {bin_number}")
    step_motor(steps, 1)
    sleep(1)
    step_motor(steps, -1)

def get_bin(label):
    label = label.lower()

    if label in ["plastic waste", "paper waste"]:
        return 1
    elif label == "organic waste":
        return 2
    elif label in ["glass waste", "light bulbs"]:
        return 3
    elif label in ["e-waste", "battery waste", "metal waste"]:
        return 4

    return 1

# ---------------- MAIN LOOP ----------------
while True:
    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            continue

        print("\nReceived:", data)

        # -------- SENSOR READ --------
        try:
            temperature = dht.temperature
            humidity = dht.humidity
        except RuntimeError:
            temperature = None
            humidity = None
            print(" Sensor retry")

        final_label = data

        # -------- SENSOR FUSION --------
        if humidity is not None:
            print(f"{temperature}°C | {humidity}%")

            if data.lower() == "organic waste" and humidity < 40:
                final_label = "paper waste"
                print("Adjusted → paper waste")

            elif data.lower() in ["e-waste", "battery waste"] and humidity > 70:
                final_label = "metal waste"
                print("Adjusted → metal waste")

            elif data.lower() == "paper waste" and humidity > 70:
                final_label = "organic waste"
                print("Adjusted → organic waste")

        print("Final Decision:", final_label)

        bin_number = get_bin(final_label)
        move_to_bin(bin_number)

    except Exception as e:
        print("ERROR:", e)