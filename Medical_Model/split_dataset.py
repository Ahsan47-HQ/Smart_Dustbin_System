import os
import random
import shutil

# ───────────── CONFIG ─────────────
SOURCE_DIR = "Dataset/Background_Removed"
DEST_DIR   = "Dataset/medical_waste"

TRAIN_SPLIT = 0.8   # 80% train, 20% test
SEED = 42

random.seed(SEED)

# ───────────── CREATE STRUCTURE ─────────────
for split in ["train", "test"]:
    for cls in os.listdir(SOURCE_DIR):
        cls_path = os.path.join(SOURCE_DIR, cls)
        if not os.path.isdir(cls_path):
            continue
        
        os.makedirs(os.path.join(DEST_DIR, split, cls), exist_ok=True)

# ───────────── SPLIT DATA ─────────────
print("\n📂 Splitting dataset...\n")

for cls in os.listdir(SOURCE_DIR):
    cls_path = os.path.join(SOURCE_DIR, cls)
    
    if not os.path.isdir(cls_path):
        continue

    images = os.listdir(cls_path)
    images = [img for img in images if not img.startswith(".")]

    random.shuffle(images)

    split_idx = int(len(images) * TRAIN_SPLIT)

    train_imgs = images[:split_idx]
    test_imgs  = images[split_idx:]

    print(f"{cls}: {len(train_imgs)} train | {len(test_imgs)} test")

    # Copy files
    for img in train_imgs:
        src = os.path.join(cls_path, img)
        dst = os.path.join(DEST_DIR, "train", cls, img)
        shutil.copy2(src, dst)

    for img in test_imgs:
        src = os.path.join(cls_path, img)
        dst = os.path.join(DEST_DIR, "test", cls, img)
        shutil.copy2(src, dst)

print("\n✅ Done splitting dataset!")