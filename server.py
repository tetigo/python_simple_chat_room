import socket
import threading

host = 'localhost'
port = 9000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()

salas = {}

def broadcast(sala, msg):
    if isinstance(msg, str):
        msg=msg.encode()
    for i in salas[sala]:
        i.send(msg)

def enviarMensagem(nome, sala, client):
    while True:
        msg = client.recv(1024)
        msg = f'{nome}: {msg.decode()}\n'
        broadcast(sala, msg)

while True:
    client, addr = server.accept()
    client.send(b'SALA')
    sala = client.recv(1024).decode()
    nome = client.recv(1024).decode()
    if sala not in salas.keys():
        salas[sala] = []
    salas[sala].append(client)
    
    broadcast(sala, f'{nome} entrou na sala\n')
    
    thread = threading.Thread(target=enviarMensagem, args=(nome, sala, client))
    thread.start()
    
    print(f'{nome} se conectou na sala {sala} - info {addr}')
    


