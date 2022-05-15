import socket
import threading

#Server parameters
HOST = '127.0.0.1'
PORT = 5432
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

clients = []
names = []

    #Handle
def handle(con, addressip):

    print(f'Connection address: {addressip}\n')
    connected = True

    while connected:
        message = con.recv(1024)
        tMsg(message)
    con.close()

    #Broadcast function
def tMsg(message):
    for client in clients:
        client.send(message)

    #Init server
def chatInit():
    server.listen()
    print(f'Server is running: {HOST}\n')

    while True:
        con, addressip = server.accept()
        con.send('NAME'.encode(FORMAT))

        name = con.recv(1024).decode(FORMAT)
        names.append(name)
        clients.append(con)
        print(f'\n{name} joinned the server.\n')

        tMsg(f'{name} joinned!\n'.encode(FORMAT))
        con.send(f'connection successful!\n'.encode(FORMAT))

        thread = threading.Thread(target=handle, args=(con, addressip))
        thread.start()

        print(f'Currently Connections: {threading.active_count() -1}\n')


chatInit()
