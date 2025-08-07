import socket

# Will only work whenn the server is also on this pc
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send("Hello World!".encode('ascii'))
print(client.recv(1024).decode('ascii'))