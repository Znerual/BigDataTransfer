import socket
import os
import tqdm
import sys
import urllib.request
import time
from scapy.layers.inet import *
from scapy.sendrecv import send


def getIp():
    ip = urllib.request.urlopen("https://api.ipify.org").read().decode('utf8')
    return ip


DESTINATION_HOST = "80.110.113.54 "
DESTINATION_PORT = 5001

SOURCE_PORT = 5001
SOURCE_HOST = "127.0.0.1"

BUFFER_SIZE = 4096
SEPARATOR = "<SEPERATOR>"

#create a TCL Handshake
#SYN
ip = IP(src=SOURCE_HOST, dst=DESTINATION_HOST)
SYN = TCP(sport=SOURCE_PORT, dport=DESTINATION_PORT, flags='S', seq=1000)
SYNACK = sr1(ip/SYN) #send the package and wait for the answer

#ACK
ACK = TCP(sport=SOURCE_PORT, dport=DESTINATION_PORT, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
send(ip/ACK)


print(f"Server gestartet mit IP Adresse {getIp()}")
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((SOURCE_HOST, SOURCE_PORT))
s.listen(5)
print(f"[*] Listening as {SOURCE_HOST}:{SOURCE_PORT}")
client_socket, address = s.accept()

print(f"[+] {address} is connected")

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for _ in progress:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break  # finished
        f.write(bytes_read)
        progress.update(len(bytes_read))

client_socket.close()
s.close()
