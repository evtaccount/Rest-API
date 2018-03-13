#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json

import Classes

def get_call():
    pass

def parse(conn, addr):
    data = b""

    while not b"\r\n" in data:
        tmp = conn.recv(1024)
        if not tmp:
            break
        else:
            data += tmp
    if not data:
        return

sock = socket.socket()
sock.bind(("", 8080))
sock.listen(1)

try:
    while 1:  # работаем постоянно
        conn, addr = sock.accept()
        print("New connection from " + addr[0])
        try:
            parse(conn, addr)
        except:
            send_answer(conn, "500 Internal Server Error", data="Ошибка")
        finally:
            # так при любой ошибке
            # сокет закроем корректно
            conn.close()
finally:
    sock.close()
# так при возникновении любой ошибки сокет
# всегда закроется корректно и будет всё хорошо
# sock = socket.socket()
# sock.bind(("", 8080))
# sock.listen(1)
# conn, addr = sock.accept()
#
# print("connected:", addr)
#
# while True:
#     data = conn.recv(1024)
#     udata = data.decode("utf-8")
#     print("Data: " + udata)
# #    if not data:
# #        print("No data")
# #        conn.close()
# #        break
#     conn.send(udata.upper().encode())
#
#
# #conn.send(b"Hello!\n")
## conn.send(b"Your data:" + udata.encode("utf-8"))

