import socket

HOST = '0.0.0.0' 
PORT = 8000

FTS = 'stuff.txt'

SSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SSocket.bind((HOST, PORT))
print(f"socket created w/ {HOST}:{PORT}...")


SSocket.listen(1)
print(f"Server listening on {HOST}:{PORT}...")

CSocket, Caddress = SSocket.accept()
print(f"Server listening on {Caddress}...")

fname = FTS.encode('utf-8')
CSocket.send(len(fname).to_bytes(4, byteorder='big'))
CSocket.send(fname)

with open(FTS, 'rb') as file:
    fileD = file.read()
    CSocket.send(len(fileD).to_bytes(4, byteorder = 'big'))
    CSocket.send(fileD)
    

CSocket.close()
SSocket.close() 


