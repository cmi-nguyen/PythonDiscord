# This is server code to send video and audio frames over TCP
import io
import socket
import threading, wave, pyaudio, pickle, struct

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9611

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), port))
s.listen(5)

clientsocket, address = s.accept()
print(f"Connection from {address} has been established")
clientsocket.send(bytes("Wellcome to the server!", "utf-8"))
msg = clientsocket.recv(1024)
print(msg)
if msg == b"Play":
    while True:
        with open('../Nu hon Bisou.mp3', 'rb') as wave_file:
            data = wave_file.read()
            a = pickle.dumps(data)
            message = struct.pack("Q", len(a)) + a
            clientsocket.sendall(message)
            break
