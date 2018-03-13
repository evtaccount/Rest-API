import socket
import json

import Classes


sock = socket.socket()
sock.connect(('localhost', 8080))
while True:
    data = input("Введите послание")
    if data:
        sock.send(data.encode())
        data = sock.recv(1024)
        udata = data.decode()
        print("Data is: ", udata)
        data = ""

sock.close()