import socket
import threading
import _thread
import tqdm
import os
import sys
import urllib.request
class HolePunching(threading.Thread):
    def __init__(self, local_port, public_port):
        self.local_host = ""
        self.local_port = local_port
        self.public_host = ""
        self.public_port = public_port
        self.punchSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.punchSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.public_host = self.getPublicIp()
        self.local_host = self.getPrivateIp()
        self.local_host = "10.0.0.6"
    def getPublicIp(self):
        ip = urllib.request.urlopen("https://api.ipify.org").read().decode('utf8')
        return ip
    def getPrivateIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # muss nicht unbedingt erreichbar sein
            s.connect(('10.255.255.255', 0))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    def run(self):
        holePunch = HolePunching(self.local_port,self.public_port)
        holePunch.RunImpl()
    def RunImpl(self):
        self.PunchHole()
        self.RunServer()

    def PunchHole(self):
        print(f"Punching hole on {self.local_host}:{self.local_port}")
        try:
            self.punchSocket.bind((self.local_host,self.local_port))
            print("Socket bound")
            self.punchSocket.connect((self.public_host,self.public_port))
            print("Hole was punched")
        except socket.error as er:
            print(f"Fehler beim Binden des Sockets {str(er)}")
            self.punchSocket.close()


    def RunServer(self):
        self.serverSocket.bind((self.local_host, self.local_port))
        self.serverSocket.listen(2)

        while (True):
            clientSocket = self.serverSocket.accept()
            _thread.start_new_thread(self.ProcessConnection(clientSocket))

    def ProcessConnection(self, connectionSocket):
        print(f"Socket accepted")
        print("Do stuff")

        connectionSocket.close()


print("Running")
HolePunching(5000,5001).run()
