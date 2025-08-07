import socket
# gets your ip adress (doesn't work if you're using virtual box)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090

#                     (type: internet, protocol: TCP/IP  )
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(5)

while True:
    communication_socket, address = server.accept()
    print(f"Connected to {address}")
    message = communication_socket.recv(1024).decode('ascii')
    print(f"The message from the client is: {message}")
    communication_socket.send(f"Message recived! Thanks!".encode('ascii'))
    communication_socket.close()
    print(f"Connection with {address} terminated!")