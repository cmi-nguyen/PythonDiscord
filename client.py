# Welcome to PyShine
# This is client code to receive video and audio frames over TCP

import socket, os
import threading, wave, pyaudio, pickle, struct

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9611

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((socket.gethostname(),port))

while True:
    msg = s.recv(1024)
    print(msg)
    s.send(bytes("Play","utf-8"))


