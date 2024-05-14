# This is server code to send video and audio frames over TCP

import socket
import threading, wave, pyaudio, pickle, struct

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9611

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), port))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established")
    clientsocket.send(bytes("Wellcome to the server!", "utf-8"))
    msg = clientsocket.recv(1024)
    print(msg)
    if msg == b"Play":
        with open('more than words.wav','rb') as wave_file:
            clientsocket.sendfile(wave_file)

