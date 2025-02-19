import socket

# Server configuration
SERVER_IP = '192.168.1.100'  # Replace with the Pi's IP address
SERVER_PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))
print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

# Receive the file name
file_name_length = int.from_bytes(client_socket.recv(4), byteorder='big')
file_name = client_socket.recv(file_name_length).decode('utf-8')
print(f"Receiving file: {file_name}")

# Receive the file size
file_size = int.from_bytes(client_socket.recv(4), byteorder='big')

# Receive the file data
file_data = b''
while len(file_data) < file_size:
    packet = client_socket.recv(file_size - len(file_data))
    if not packet:
        break
    file_data += packet

# Save the file
with open(file_name, 'wb') as file:
    file.write(file_data)

print(f"File '{file_name}' received and saved successfully.")

# Close the connection
client_socket.close()