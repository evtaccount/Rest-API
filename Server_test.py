#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import uuid
import time


keys = ["id", "title", "text", "date_create", "date_update"]


# Данная фенкция формирует ответ клиенту в формате словаря с необходимыми ключами
def send_answer(uuid_note="", title="", text="", date_create=0000000000, date_update=0000000000):
    send_data = {"id": uuid_note, "title": title, "text": text, "date_create": date_create, "date_update": date_update}
    tmp_data = json.dumps(send_data).encode()
    return tmp_data


#Функция считывает из файла все заметки и возвращает список словарей
def get_notes():
    notes = []
    current_note = {}
    try:
        with open("notes.txt", encoding='utf-8') as f:
            for note in f:
                note = note.strip().split(',')
                for n, item in enumerate(keys):
                    current_note[item] = note[n]
                notes.append(current_note.copy())
    except:
        return notes


#Функция записывает новую заметку в файл. В случае успеха возвращает True; если запись не выполнена - возвращает False
def save_note(new_note):
    tmp = []
    saved_note = []
    new_note["id"] = str(uuid.uuid4())
    new_note["date_create"] = int(time.time())
    new_note["date_update"] = int(time.time())

    for key in new_note:
        tmp.append(str(new_note[key]))
    tmp = ','.join(tmp)

    try:
        with open("notes.txt", "a", encoding='utf-8') as f:
            f.write(tmp + '\n')
            print("Заметка успешно создана")
            saved_note = tmp.strip().split(",")
    except:
        print("Ошибка записи")
    finally:
        return saved_note


#Функция принимает в качестве аргументов список словарей и id нужного словаря. Словарь с этим id удаляет из списка.
def del_note(selected_id):
    readed_notes = get_notes()
    deleted_note = []
    for ind, tmp_note in enumerate(readed_notes):
        if tmp_note["id"] == selected_id:
            tmp_note = readed_notes.pop(ind)
            save_all(readed_notes)
            break
    for key in tmp_note.keys():
        deleted_note.append(tmp_note[key])
    return deleted_note


#Функция принимает в качестве аргументов список словарей и отредактированный словарь. Заменяет в списке в искомом
#словаре "title" и "text" на новые. При этом обновляется "date_update". Возвращается отредактированный список словарей.
def replace_note(new_note):
    replaced_note = []
    readed_notes = get_notes()
    for note in readed_notes:
        if new_note["id"] == note["id"]:
            note["title"] = new_note["title"]
            note["text"] = new_note["text"]
            note["date_update"] = str(int(time.time()))
            replaced_note = note
            break
    save_all(readed_notes)
    return replaced_note


#Принимает в качестве аргумента список словарей и записывает из в файл
def save_all(notes_to_save):
    with open("notes.txt", "w", encoding="utf-8") as f:
        for ind, note in enumerate(notes_to_save):
            tmp = []
            for key in note:
                tmp.append(note[key])
            f.write(','.join(tmp) + '\n')


sock = socket.socket()
sock.bind(('localhost', 8080))
sock.listen(1)
conn, addr = sock.accept()
print("connected:", addr)

while True:
    data = conn.recv(1024)
    recieved_data = json.loads(data.decode("utf-8"))

    #Добавить заметку
    if recieved_data["id"] == "" and recieved_data["title"] != "":
        note = save_note(recieved_data)
        conn.sendall(send_answer(*note))

    # Показать имеющиеся заметки
    elif recieved_data["id"] == "" and recieved_data["title"] == "":
        notes = get_notes()
        answer = json.dumps(notes).encode()
        conn.sendall(answer)

    # Удалить заметку
    elif recieved_data["id"] != "" and recieved_data["title"] == "":
        note = del_note(recieved_data["id"])
        print("note", note)
        conn.sendall(send_answer(*note))

    # Изменить заметку
    elif recieved_data["id"] != "" and recieved_data["title"] != "" and recieved_data["text"] != "":
        note = replace_note(new_note=recieved_data)
        conn.sendall(send_answer(*note))
