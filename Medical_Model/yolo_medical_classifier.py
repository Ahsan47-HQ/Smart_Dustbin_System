import cv2
import numpy as np
import tensorflow as tf
from ultralytics import YOLO
import tensorflow as tf
import keras
from keras.applications.efficientnet_v2 import preprocess_input

# ──────────────── LOAD MODELS ────────────────

print("Loading YOLO...")
yolo_model = YOLO("yolov8n.pt")

print("Loading EfficientNet...")

def build_model(num_classes):
    from keras.applications import EfficientNetV2B0
    from keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
    from keras.models import Model

    base = EfficientNetV2B0(weights=None, include_top=False, input_shape=(240, 240, 3))

    x = base.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)
    x = Dense(256, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(0.3)(x)

    outputs = Dense(num_classes, activation="softmax", dtype="float32")(x)

    return Model(inputs=base.input, outputs=outputs)


# 🔥 YOUR 5 CLASSES
CLASS_NAMES = [
    "biohazard",
    "glass",
    "metal",
    "plastic",
    "sharps"
]

model = build_model(len(CLASS_NAMES))
model.load_weights("smart_dustbin_model.weights.h5")

print("✅ Model ready!")

# ──────────────── CAMERA ────────────────

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

YOLO_CONF = 0.4

# ──────────────── LOOP ────────────────

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    results = yolo_model(frame, verbose=False)

    for result in results:
        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])

            if conf < YOLO_CONF:
                continue

            # Clamp bounds
            x1, x2 = max(0, x1), min(w, x2)
            y1, y2 = max(0, y1), min(h, y2)

            if x2 - x1 < 10 or y2 - y1 < 10:
                continue

            # ── Crop ──
            crop = frame[y1:y2, x1:x2]

            crop = cv2.resize(crop, (240, 240))
            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

            crop = preprocess_input(np.expand_dims(crop.astype(np.float32), axis=0))

            # ── Predict ──
            preds = model.predict(crop, verbose=0)[0]

            idx = np.argmax(preds)
            label = CLASS_NAMES[idx]
            conf_class = preds[idx]

            # ── Draw ──
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            text = f"{label} ({conf_class*100:.1f}%)"

            cv2.putText(frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Medical Waste Classifier", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()