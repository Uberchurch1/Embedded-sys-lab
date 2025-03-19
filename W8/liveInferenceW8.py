import time
import torch
import numpy as np
from torchvision import models, transforms
import cv2
import math
import os
from flask import Flask, Response
import threading
from PIL import Image
import json
import requests

torch.backends.quantized.engine = 'qnnpack'

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

net = models.quantization.mobilenet_v2(pretrained=True, quantize=True)


# Load ImageNet class labels from a URL
imagenet_url = "https://storage.googleapis.com/download.tensorflow.org/data/imagenet_class_index.json"
response = requests.get(imagenet_url)
class_idx = response.json()

# Convert class labels to a list for easy access
class_names = [class_idx[str(i)][1] for i in range(1000)]

# Set the QT platform for GUI to avoid Wayland issues
os.environ["QT_QPA_PLATFORM"] = "xcb"

# Initialize Flask app for serving the image
app = Flask(__name__)

# Path to save the processed image
image_path = "output_image.jpg"

# Start webcam
cap = cv2.VideoCapture(0)  # Change the index if needed
cap.set(3, 640)  # Set video frame width to 640
cap.set(4, 480)  # Set video frame height to 480

# jit model to take it from ~20fps to ~30fps
net = torch.jit.script(net)

started = time.time()
last_logged = time.time()
frame_count = 0

def generate():
    global frame_count  # Declare frame_count as global
    global last_logged
    global started 
    with torch.no_grad():
        while True:
            # Read frame
            ret, image = cap.read()
            if not ret:
                raise RuntimeError("failed to read frame")

            # Convert OpenCV output from BGR to RGB
            image_rgb = image[:, :, [2, 1, 0]]  # Convert from BGR to RGB

            # Preprocess image for model input
            input_tensor = preprocess(image_rgb)

            # Create a mini-batch as expected by the model
            input_batch = input_tensor.unsqueeze(0)

            # Run model to get predictions (logits)
            outputs = net(input_batch)

            # Apply softmax to get probabilities (confidence)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)

            # Get the predicted class (index of max probability)
            confidence, predicted_class = torch.max(probabilities, 1)

            # Convert confidence to a percentage
            confidence = confidence.item()

            # Get class name based on the predicted class index
            class_name = class_names[predicted_class.item()]

            print(f"Predicted Class: {class_name}, Confidence: {confidence:.4f}")

            # Draw the bounding box on the image (example: fixed size)
            cv2.rectangle(image, (0, 0), (400, 30), (255, 0, 255), -1)

            # Display the class name and confidence at the top of the bounding box
            org = (0, 25)  # Position slightly above the bounding box
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (0, 0, 0)
            thickness = 2
            cv2.putText(image, f"{class_name} {confidence:.2f}", org, font, fontScale, color, thickness)

            # Save the processed frame as an image (could be used for fallback)
            cv2.imwrite(image_path, image)  # Save the processed image to disk

            # Encode the image as JPEG and send it over HTTP
            ret, jpeg = cv2.imencode('.jpg', image)
            if not ret:
                break
            frame = jpeg.tobytes()

            # Yield the frame to the browser as part of a streaming response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            # Log model performance
            frame_count += 1  # Increment the global frame_count
            now = time.time()
            if now - last_logged > 1:
                print(f"{frame_count / (now-last_logged)} fps")
                last_logged = now
                frame_count = 0


# Route to stream the video to browser
@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Run Flask server in a separate thread
def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Allow Flask to run in the background
    flask_thread.start()

    # Main loop to process frames and stream them to the browser
    # This will now be handled by the Flask app
    while True:
        pass
