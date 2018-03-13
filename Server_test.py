#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import uuid
import time

import Classes
import Functions


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
        Functions.save_note(recieved_date)

    # Показать имеющиеся заметки
    if recieved_date["id"] == "" and recieved_date["title"] == "":
        notes = Functions.get_notes()
        data = json.dumps(notes).encode()
        conn.sendall(data)

    # Удалить заметку
    if recieved_date["id"] != "" and recieved_date["title"] == "":
        print("Here is ok")
        notes = Functions.get_notes()
        Functions.del_note(notes, recieved_date["id"])

    # Изменить заметку
    if recieved_date["id"] != "" and recieved_date["title"] != "" and recieved_date["text"] != "":
        print("recieved date - ", recieved_date)
        print("Edit here")
        notes = Functions.get_notes()
        print("replaced note list", Functions.replace_not(note_list=notes, new_note=recieved_date))
