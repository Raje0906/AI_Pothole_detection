import cv2
import torch
from ultralytics import YOLO
import os

# Load YOLOv8 model
model = YOLO("models/yolov8n.pt")

def detect_potholes(input_path, is_video=False):
    output_path = f"static/detections/{os.path.basename(input_path)}"
    
    if not is_video:
        # Process Image
        image = cv2.imread(input_path)
        results = model(input_path)  # Run YOLO on image
        
        print("Detection Results:", results)  # Debugging output

        for result in results:
            for box in result.boxes.xyxy:  # Bounding box coordinates (x1, y1, x2, y2)
                x1, y1, x2, y2 = map(int, box[:4])
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
        
        cv2.imwrite(output_path, image)  # Save annotated image
        return output_path, results  # Return path & detection data
