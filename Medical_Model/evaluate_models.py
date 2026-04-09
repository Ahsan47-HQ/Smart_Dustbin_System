import os
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# ───────── CONFIG ─────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRAIN_DIR = os.path.join(BASE_DIR, "Dataset", "medical_waste", "train")
TEST_DIR  = os.path.join(BASE_DIR, "Dataset", "medical_waste", "test")

MODEL_BEST = os.path.join(BASE_DIR, "smart_dustbin_model_best.keras")
MODEL_LAST = os.path.join(BASE_DIR, "smart_dustbin_model_last.keras")

IMG_SIZE = (240, 240)
BATCH_SIZE = 32

# ───────── LOAD DATA ─────────
def load_dataset(path):
    return tf.keras.utils.image_dataset_from_directory(
        path,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
        shuffle=False
    )

# ───────── EVALUATION FUNCTION ─────────
def evaluate_model(model, dataset, name, class_names):
    print("\n" + "="*50)
    print(f"Evaluating: {name}")
    print("="*50)

    loss, acc = model.evaluate(dataset, verbose=1)
    print(f"\nAccuracy: {acc*100:.2f}% | Loss: {loss:.4f}")

    # Predictions
    y_pred_probs = model.predict(dataset)
    y_pred = np.argmax(y_pred_probs, axis=1)

    y_true = np.concatenate([
        np.argmax(y.numpy(), axis=1)
        for _, y in dataset
    ])

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(6,6))
    plt.imshow(cm, cmap="Blues")
    plt.title(f"{name} Confusion Matrix")
    plt.colorbar()

    ticks = np.arange(len(class_names))
    plt.xticks(ticks, class_names, rotation=45)
    plt.yticks(ticks, class_names)

    for i in range(len(class_names)):
        for j in range(len(class_names)):
            plt.text(j, i, cm[i, j], ha="center", va="center")

    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()

    save_path = f"{name.replace(' ', '_')}_cm.png"
    plt.savefig(save_path)
    plt.close()

    print(f"Saved confusion matrix: {save_path}")

# ───────── MAIN ─────────
def main():
    print("\n📂 Loading datasets...")
    train_ds = load_dataset(TRAIN_DIR)
    test_ds  = load_dataset(TEST_DIR)

    class_names = train_ds.class_names
    print(f"\nClasses: {class_names}")

    print("\n📦 Loading models...")
    model_best = tf.keras.models.load_model(MODEL_BEST)
    model_last = tf.keras.models.load_model(MODEL_LAST)

    # ───────── EVALUATE ─────────
    evaluate_model(model_best, train_ds, "BEST_MODEL_TRAIN", class_names)
    evaluate_model(model_best, test_ds,  "BEST_MODEL_TEST",  class_names)

    evaluate_model(model_last, train_ds, "LAST_MODEL_TRAIN", class_names)
    evaluate_model(model_last, test_ds,  "LAST_MODEL_TEST",  class_names)

    print("\n✅ Done evaluating both models.")

if __name__ == "__main__":
    main()