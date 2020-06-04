import socket
import os
import tqdm
import sys

SEPERATOR = "<SEPERATOR>"
BUFFER_SIZE = 4096

#host = "192.168.1.101" #receiver ip adress
port = 5001

if (len(sys.argv) >  2):
    filename = sys.argv[1]
    host = sys.argv[2]
else:
    print(f"Das Inputformat stimmt nicht. Bitte zuerst Dateinamen, dann Empfänger IP-Adresse angeben")
    sys.exit()

filesize = os.path.getsize(filename)

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
print(f"[+]Connecting to {host}:{port}")
s.connect((host, port))
print(f"[+]Connected")

s.send(f"{filename}{SEPERATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B",  unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break #finished reading

        s.sendall(bytes_read)
        progress.update(len(bytes_read))
s.close()