#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import uuid
import time

import Classes
import Funcions


# def recieve_note(host):
#     data = b""
#     while not b"\r\n" in data:
#         tmp = host.recv(1024)
#         if not data:
#             break
#         else:
#             data += tmp
#     return json.loads(data.decode("utf-8"))


sock = socket.socket()
sock.bind(("", 8080))
sock.listen(1)
conn, addr = sock.accept()
print("connected:", addr)

while True:
    data = conn.recv(1024)
    recieved_date = json.loads(data.decode("utf-8"))

    #Добавить заметку
    if recieved_date["id"] == "" and recieved_date["title"] != "":
        recieved_date["id"] = str(uuid.uuid4())
        recieved_date["date_create"] = int(time.time())
        recieved_date["date_update"] = int(time.time())
        Funcions.save_note(recieved_date)

    # Показать имеющиеся заметки
    if recieved_date["id"] == "" and recieved_date["title"] == "":
        notes = Funcions.get_notes()
        data = json.dumps(notes).encode()
        conn.sendall(data)

    # Удалить заметку
    if recieved_date["id"] != "" and recieved_date["title"] == "":
        print("Here is ok")

    # Изменить заметку
    if recieved_date["id"] != "" and recieved_date["title"] != "":
        pass
    # if command == "get_notes":
    #     notes = Funcions.get_notes()
    #     print(notes)
    #
    #     data = json.dumps(notes).encode()
    #     conn.sendall(data)
    #     print(data)
    # if command == "delete_note":
    #     pass
    # if command == "update_note":
    #     pass

# while True:
#     data = conn.recv(1024)
#     # udata = data.decode("utf-8")
#     udata = json.loads(data.decode("utf-8"))
#     udata["id"] = str(uuid.uuid4())
#     print(udata)
#     if not data:
#         print("No data")
#         conn.close()
#         break
#     conn.send(json.dumps(udata).encode())


#conn.send(b"Hello!\n")
# conn.send(b"Your data:" + udata.encode("utf-8"))

