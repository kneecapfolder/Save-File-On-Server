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

        communication_socket.send(names.encode('utf-8'))
    else:
        communication_socket.send('empty'.encode('utf-8'))

    print(communication_socket.recv(1024).decode('utf-8'))




# Send file to client
def get(communication_socket):
    communication_socket.send(f'action accepted!'.encode('utf-8'))

    filename = communication_socket.recv(1024).decode('utf-8')
    print(f'filename is: {filename}')
    
    bin_data = ''
    size = 1024

    # Check if file exists
    try:
        with open(f'server/storage/{filename}', 'rb') as file:
            bin_data = file.read()
            file.seek(0, os.SEEK_END)
            size = file.tell() 
            communication_socket.send('found!'.encode('utf-8'))
            print(communication_socket.recv(1024).decode('utf-8'))
    except:
        communication_socket.send('error!'.encode('utf-8'))
        print(communication_socket.recv(1024).decode('utf-8'))
        return


    communication_socket.send(f'{size}'.encode('utf-8'))
    print(communication_socket.recv(1024).decode('utf-8'))

    communication_socket.send(bin_data)
    print(communication_socket.recv(1024).decode('utf-8'))



# Save file to storage
def upload(communication_socket):
    communication_socket.send(f'action accepted!'.encode('utf-8'))
    
    size = int(communication_socket.recv(1024).decode('utf-8'))
    communication_socket.send(f'file size is {size}!'.encode('utf-8'))
    print(f"file size is {size}!")
    
    filename = communication_socket.recv(1024).decode('utf-8')
    communication_socket.send(f'The file name is {filename}'.encode('utf-8'))
    print(f"The file name is {filename}")

    # Get the datat in binary
    file_data = communication_socket.recv(size)

    with open(f'server/storage/{filename}', 'wb') as file:
        file.write(file_data)

    print("file saved!")






communication_socket, address = server.accept()
print(f"Connected to {address}")

while True:

    action = communication_socket.recv(1024).decode('utf-8')
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
    # message = communication_socket.recv(1024).decode('utf-8')
    # print(f"The message from the client is: {message}")
    # communication_socket.send(f"Message recived! Thanks!".encode('utf-8'))
    # communication_socket.close()
    # print(f"Connection with {address} terminated!")