import socket
import os
import tqdm

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT,1)

s.bind(("0.0.0.0", 5000))
