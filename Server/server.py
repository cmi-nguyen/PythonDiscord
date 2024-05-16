# This is server code to send video and audio frames over TCP
import os.path
import pickle
import socket
import struct
from pathlib import Path


def server():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print(host_ip)
    port = 9611

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), port))
    s.listen(5)

    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established")
        clientsocket.send(bytes("Wellcome to the server!", "utf-8"))

        msg = clientsocket.recv(1024)
        song_name = clientsocket.recv(1024).decode("utf-8")
        print(msg)
        if msg == b"Search":
            os_path = './song/' + song_name + '.mp3'
            print(os.path.exists(os_path))
            if os.path.exists(os_path):
                clientsocket.send(bytes('200', "utf-8"))
            else:
                clientsocket.send(bytes('404', "utf-8"))
            clientsocket.close()
        if msg == b"queue":
            song_name_list = []

        if msg == b"Play":
            # song = 'Nu hon Bisou.mp3'
            os_path = './song/' + song_name + '.mp3'
            print(os_path)
            if os.path.exists(os_path):
                file_bytes = Path('./song/' + song_name + '.mp3').read_bytes()
                data = file_bytes
                a = pickle.dumps(data)
                message = struct.pack("Q", len(a)) + a
                clientsocket.sendall(message)
                clientsocket.close()




if __name__ == '__main__':
    server()
