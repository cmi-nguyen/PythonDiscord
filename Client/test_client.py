# Welcome to PyShine
# This is client code to receive video and audio frames over TCP

import pickle
import socket
import struct

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9611


def audio_stream():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), port))

    msg = s.recv(1024)
    print(msg)
    s.send(bytes("Play", "utf-8"))
    data = b""
    payload_size = struct.calcsize("Q")
    stream = open("../test.mp3", 'wb')
    stream.write(b'')
    while True:
        try:
            while len(data) < payload_size:
                packet = s.recv(4 * 1024)  # 4K
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += s.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            stream.write(frame)

        except:

            break

    s.close()
    print('Audio Created')
