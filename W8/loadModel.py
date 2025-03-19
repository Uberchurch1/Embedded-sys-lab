import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import time  # Importing time module

# Set parameters
batch_size = 1  # Only one image to test at a time
num_epochs = 10
learning_rate = 0.01

model_path = "/home/Group6/Embedded Lab/W8/fashion_mnist_optimized.pth"
image_path = "/home/Group6/Embedded Lab/W8/sandal.jpg"

device = torch.device("cpu")
criterion = nn.CrossEntropyLoss()

# Define a simple neural network
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(28*28, 128)  # Input size is 28x28 images (FashionMNIST)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)  # 10 output classes

    def forward(self, x):
        x = x.view(-1, 28*28)  # Flatten the input image
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Load model
model = SimpleNN().to(device)
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((28, 28)),  # Resize the image to 28x28 pixels (FashionMNIST size)
    transforms.Grayscale(num_output_channels=1),  # Ensure it's grayscale
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))  # Mean and Std of MNIST dataset
])

# Load the image
img = Image.open(image_path).convert('RGB')  # Open image
img = transform(img).unsqueeze(0)  # Apply transformations and add batch dimension

# Create a DataLoader with the image
test_loader = torch.utils.data.DataLoader([img], batch_size=batch_size)

# Class names for FashionMNIST dataset (adjust if needed)
class_names = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
]

# Test function with inference time
def test(model, device, test_loader, criterion):
    model.eval()
    test_loss = 0.0
    test_acc = 0.0
    with torch.no_grad():
        start_time = time.time()  # Record start time
        for inputs in test_loader:
            inputs = inputs.to(device)  # Move to device
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            predicted_class = predicted.item()
            print(f"Class name: {class_names[predicted_class]}")  # Display class name
        end_time = time.time()  # Record end time

        # Calculate and print inference time
        inference_time = end_time - start_time
        print(f"Inference time: {inference_time:.4f} seconds")  # Print inference time

# Run test
test(model, device, test_loader, criterion)
