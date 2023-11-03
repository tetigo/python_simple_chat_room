import socket
import threading
from tkinter import *
import tkinter
from tkinter import simpledialog

host = 'localhost'
port = 9000

class Chat:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        login = Tk()
        login.withdraw()
        
        self.janela_carregada = False
        self.ativo = True
        
        self.nome = simpledialog.askstring('Nome','digite seu nome', parent=login)
        self.sala = simpledialog.askstring('Sala','digite a sala que deseja entrar', parent=login)
        
        thread = threading.Thread(target=self.conecta)
        thread.start()
        
        self.janela()

    def janela(self):
        self.root = Tk()
        self.root.geometry("700x600")
        self.root.title("Chat")
        
        self.caixa_texto = Text(self.root)
        self.caixa_texto.place(relx=0.05, rely=0.01, width=500, height=450)
        
        self.envia_mensagem = Entry(self.root)
        self.envia_mensagem.place(relx=0.05, rely=0.8, width=500, height=20)
        
        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviarMSG)
        self.btn_enviar.place(relx=0.82, rely=0.8, width=100, height=20)
        
        self.root.protocol('WM_DELETE_WINDOW', self.fechar)
        
        self.root.mainloop()


    def fechar(self):
        self.root.destroy()
        self.client.close()

    def conecta(self):
        while True:
            recebido = self.client.recv(1024)
            if recebido == b'SALA':
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    self.caixa_texto.insert('end', recebido.decode())
                except:
                    pass

    def enviarMSG(self):
        msg = self.envia_mensagem.get()
        self.client.send(msg.encode())

chat = Chat()    
