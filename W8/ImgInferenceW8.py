import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import cv2
import numpy as np
import time

# Update model to match the saved one
class FashionMNISTModel(nn.Module):
    def __init__(self):
        super(FashionMNISTModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        # Update the size of fc1 according to your saved model
        self.fc1 = nn.Linear(128 * 7 * 7, 128)  # Adjust fc1 input dimension if needed
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2)
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2)
        x = torch.relu(self.conv3(x))
        x = torch.max_pool2d(x, 2)
        x = x.view(x.size(0), -1)  # Flatten the output
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# The rest of the code remains the same


# Function to preprocess the image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized_img = cv2.resize(gray_img, (28, 28))
    enhanced_img = cv2.equalizeHist(resized_img)
    normalized_img = enhanced_img / 255.0
    normalized_img = (normalized_img - 0.1307) / 0.3081
    img_tensor = np.expand_dims(normalized_img, axis=0)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    return img_tensor


# Inference function
def run_inference(model, image_tensor, device):
    model.eval()
    image_tensor = torch.tensor(image_tensor, dtype=torch.float32).to(device)
    start_time = time.time()

    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted_class = torch.max(outputs, 1)

    end_time = time.time()
    inference_time = end_time - start_time
    return predicted_class.item(), inference_time


# Main function to process image and run inference
def main():
    image_path = "/home/Group6/Downloads/purse.jpg"  # Update with the path of your image
    model_path = "/home/Group6/Embedded Lab/W8/fashion_mnist_optimized.pth"

    # Load the trained model
    model = FashionMNISTModel()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    
    # Device
    device = torch.device("cpu")
    model.to(device)

    # Preprocess image
    preprocessed_image = preprocess_image(image_path)

    # Run inference
    predicted_class, inference_time = run_inference(model, preprocessed_image, device)

    # Print results
    print(f"Predicted class: {predicted_class}")
    print(f"Inference time: {inference_time:.4f} seconds")


if __name__ == "__main__":
    main()
