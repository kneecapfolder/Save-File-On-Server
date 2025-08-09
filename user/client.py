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
    client.send("close".encode())
    client.close()



def list_storage():
    
    client.send("list".encode())
    
    names = client.recv(1024).decode()
    list = [name for name in names.split('\n') if name != ''] if names != 'empty' else []


    client.send("list recived!".encode())

    return list





def get_file(filename):
    
    client.send("get".encode())
    print(client.recv(1024).decode())

    client.send(filename.encode())

    if client.recv(1024).decode() == 'error!':
        client.send('error exepted'.encode())
        return False

    # File exists on server
    client.send('can continue'.encode())

    chunk_count = int(client.recv(1024).decode())
    client.send(f'got chunk count! ({chunk_count})'.encode())

    chunks = []
    for _ in range(chunk_count):
        chunks.append(client.recv(1024))

    client.send('got file data!'.encode())

    # print(bin_data)
    return chunks





def upload_file(path):
    try:
        with open(path, 'rb') as file:

            # Tell the server you're uploading
            client.send('upload'.encode())
            print(client.recv(1024).decode())

            # Give the filename
            client.send(path.split('/')[-1].encode())
            print(client.recv(1024).decode())

            chunks_lst = []
            
            chunk = file.read(1024)
            while chunk:
                chunks_lst.append(chunk)
                chunk = file.read(1024)

            client.send(f'{len(chunks_lst)}'.encode())
            print(client.recv(1024).decode())

            for chunk in chunks_lst:
                client.send(chunk)


            print(client.recv(1024).decode())
    
            
            
            return True

    except FileNotFoundError:
        print(f"The file at {path} was not found.")
        return False
