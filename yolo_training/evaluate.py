from ultralytics import YOLO

# Load trained model
model = YOLO("runs/detect/train/weights/best.pt")

# Validate on test set
metrics = model.val(data="datasets/data.yaml", imgsz=640)
print(metrics)  # dict of mAP, precision, recall, etc.

# Run inference on images
results = model.predict(source="test_images/", imgsz=640, conf=0.25)
