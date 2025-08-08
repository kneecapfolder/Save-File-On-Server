import os
import socket

# Will only work whenn the server is also on this pc
HOST = open('./server-ip.txt', 'r').read()
PORT = int(open('./port-num.txt', 'r').read())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start():
    try:
        client.connect((HOST, PORT))
    except:
        return False
    
    return True

def close_app():
    client.send("close".encode('utf-8'))



def list_storage():
    
    client.send("list".encode('utf-8'))
    
    names = client.recv(1024).decode('utf-8')
    list = [name for name in names.split('\n') if name != ''] if names != 'empty' else []


    client.send("list recived!".encode('utf-8'))

    return list





def get_file(filename):
    
    client.send("get".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

    client.send(filename.encode('utf-8'))

    if client.recv(1024).decode('utf-8') == 'error!':
        client.send('error exepted'.encode('utf-8'))
        return False

    client.send('can continue'.encode('utf-8'))

    size = int(client.recv(1024).decode('utf-8'))
    client.send(f'got file size! ({size})'.encode('utf-8'))

    bin_data = client.recv(size)
    client.send('got file data!'.encode('utf-8'))

    # print(bin_data)
    return bin_data





def upload_file(path):
    bin_data = ''
    size = 1024

    # read file from path
    try:
        with open(path, 'rb') as file:
            bin_data = file.read()
            file.seek(0, os.SEEK_END)
            size = file.tell() 
    except FileNotFoundError:
        print(f"The file at {path} was not found.")
        return False
    
    # print(bin_data)
    
    # Tell the server you're uploading
    client.send('upload'.encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

    client.send(f'{size}'.encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

    # Give the filename
    client.send(path.split('/')[-1].encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

    client.send(bin_data)

    return True

    









# client.send("Hello World!".encode('utf-8'))
# print(client.recv(1024).decode('utf-8'))