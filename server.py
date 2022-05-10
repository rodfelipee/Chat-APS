import socket
import threading

HOST = '127.0.0.1'
PORT = 5432
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

clients = []
names = []


def handle(con, addressip):

    print(f'Connection address: {addressip}\n')
    connected = True

    while connected:
        message = con.recv(1024)
        terminalMsg(message)
    con.close()


def terminalMsg(message):
    for client in clients:
        client.send(message)


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

        terminalMsg(f'{name} joinned!\n'.encode(FORMAT))
        con.send(f'connection successful!\n'.encode(FORMAT))

        thread = threading.Thread(target=handle, args=(con, addressip))
        thread.start()

        print(f'Currently Connections: {threading.active_count() -1}\n')


chatInit()
