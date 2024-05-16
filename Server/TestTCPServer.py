#!/usr/bin/env python3

import pathlib
import socket

from flask import Flask, redirect, send_from_directory

app = Flask(__name__)

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9611
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), port))


@app.route("/stream", methods=("GET",))
def playlist():
    return redirect("/stream/playlist.m3u8")


@app.route("/stream/<path:name>", methods=("GET",))
def get_stream_data(name):
    return send_from_directory(pathlib.Path.cwd() / "stream", name)


@app.route("/stream/play", methods=["PUT"])
def play():
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #    s.connect((HOST, PORT))
    method = "PLAY"
    s.sendall(str.encode(method))
    # data = s.recv(1024)

    # print(f'Received {data!r}')
    return "200 OK"


@app.route("/stream/pause", methods=["PUT"])
def pause():
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #    s.connect((HOST, PORT))
    method = "PAUSE"
    s.sendall(str.encode(method))
    # data = s.recv(1024)

    # print(f'Received {data!r}')
    return "200 OK"


@app.route("/stream/skip", methods=["PUT"])
def skip():
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #    s.connect((HOST, PORT))
    method = "SKIP"
    s.sendall(str.encode(method))
    # data = s.recv(1024)

    # print(f'Received {data!r}')
    return "200 OK"


if __name__ == "__main__":
    # TODO: use a real WSGI server for production
    app.run()
