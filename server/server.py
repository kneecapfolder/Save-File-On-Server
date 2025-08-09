import os
import socket
# gets your ip adress (doesn't work if you're using virtual box)
HOST = socket.gethostbyname(socket.gethostname())
PORT = int(open('./port-num.txt', 'r').read())

#                     (type: internet, protocol: TCP/IP  )
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen(5)

# List files in storage
def lst(communication_socket):
    path = 'server/storage'
    names = ''
    dir = os.listdir(path)

    if dir:
        for filename in dir:
            names += f'{filename}\n'

        communication_socket.send(names.encode())
    else:
        communication_socket.send('empty'.encode())

    print(communication_socket.recv(1024).decode())




# Send file to client
def get(communication_socket):
    communication_socket.send(f'action accepted!'.encode())

    filename = communication_socket.recv(1024).decode()
    print(f'filename is: {filename}')
    
    chunks_list = []

    # Check if file exists
    try:
        with open(f'server/storage/{filename}', 'rb') as file:
            chunk = file.read(1024)
            while chunk:
                chunks_list.append(chunk)
                chunk = file.read(1024)

            communication_socket.send('found!'.encode())
            print(communication_socket.recv(1024).decode())
    except:
        communication_socket.send('error!'.encode())
        print(communication_socket.recv(1024).decode())
        return

    communication_socket.send(f'{len(chunks_list)}'.encode())
    print(communication_socket.recv(1024).decode())

    for chunk in chunks_list:
        communication_socket.send(chunk)
    
    print(communication_socket.recv(1024).decode())



# Save file to storage
def upload(communication_socket):
    communication_socket.send(f'action accepted!'.encode())
    
    filename = communication_socket.recv(1024).decode()
    communication_socket.send(f'The file name is {filename}'.encode())
    print(f"The file name is {filename}")


    chunk_count = int(communication_socket.recv(1024).decode())
    communication_socket.send(f'got chunk count! ({chunk_count})'.encode())

    with open(f'server/storage/{filename}', 'wb') as file:
        for _ in range(chunk_count):
            file.write(communication_socket.recv(1024))

            
    print("file saved!")
    communication_socket.send('got the file'.encode())




communication_socket, address = server.accept()
print(f"Connected to {address}")

while True:

    action = communication_socket.recv(1024).decode()
    print(f"action: {action}")

    if action == 'list':
        lst(communication_socket)
    elif action == 'get':
        get(communication_socket)
    elif action == 'upload':
        upload(communication_socket)
    elif action == 'close':
        communication_socket.close()
        print(f"Connection with {address} terminated!")
        
        communication_socket, address = server.accept()
        print(f"Connected to {address}")
    





    # communication_socket, address = server.accept()
    # print(f"Connected to {address}")
    # message = communication_socket.recv(1024).decode()
    # print(f"The message from the client is: {message}")
    # communication_socket.send(f"Message recived! Thanks!".encode())
    # communication_socket.close()
    # print(f"Connection with {address} terminated!")