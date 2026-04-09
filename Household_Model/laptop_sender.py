import cv2
import numpy as np
import tensorflow as tf
from ultralytics import YOLO
from tensorflow.keras.applications.efficientnet_v2 import preprocess_input
import socket, pickle, struct, time

yolo_model = YOLO("yolov8n.pt")

# ── ADDED: Confidence threshold (same as yolo_classifier.py) ──
YOLO_CONF_THRESH = 0.4

def build_model_architecture(num_classes):
    from tensorflow.keras.applications import EfficientNetV2B0
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
    from tensorflow.keras.models import Model

    base_model = EfficientNetV2B0(weights=None, include_top=False, input_shape=(240, 240, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    x = Dense(256, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)
    predictions = Dense(num_classes, activation="softmax", dtype="float32")(x)
    return Model(inputs=base_model.input, outputs=predictions)

CLASS_NAMES = [
    "E-waste", "battery waste", "glass waste", "light bulbs",
    "metal waste", "organic waste", "paper waste", "plastic waste"
]

classifier_model = build_model_architecture(len(CLASS_NAMES))
classifier_model.load_weights("smart_dustbin_model.weights.h5")

# STREAM SERVER
HOST = "0.0.0.0"
PORT_STREAM = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT_STREAM))
server.listen(1)

print("Waiting for Pi camera...")
conn, _ = server.accept()

# PI CONNECTION
PI_IP = "172.20.10.13"   # CHANGE
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((PI_IP, PORT))

data = b""
payload_size = struct.calcsize("Q")

last_sent = 0

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)

    if frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # ── UPDATED: Added confidence threshold here ──
    results = yolo_model(frame, verbose=False, conf=YOLO_CONF_THRESH)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            resized = cv2.resize(crop, (240, 240))
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            img = preprocess_input(np.expand_dims(rgb.astype(np.float32), axis=0))

            preds = classifier_model.predict(img, verbose=0)
            label = CLASS_NAMES[np.argmax(preds)]

            if time.time() - last_sent > 2:
                client.send((label + "\n").encode())
                print("📤 Sent:", label)
                last_sent = time.time()

            break

    cv2.imshow("AI Feed", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()