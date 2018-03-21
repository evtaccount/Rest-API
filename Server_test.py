#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import uuid
import time

import Classes
import Functions


note_template = {
    "id": "",
    "title": "",
    "text": "",
    "date_create": 0,
    "date_update": 0
}


#Функция принимает заданные аршументы (незаданные остаются по дефолту) и формирует строку для передаяи по сети,
#переводя в json и кодируя
def send_note(id="", title="", text="", date_create=0000000000, date_update=0000000000):
    send_data = {"id": id, "title": title, "text": text, "date_create": date_create, "date_update": date_update}
    data = json.dumps(send_data).encode()
    return data


#Функция считывает из файла все заметки и возвращает список словарей
def get_notes():
    notes = []
    current_note = {}
    with open("notes.txt", encoding='utf-8') as f:
        for note in f:
            note = note.strip().split(',')
            for n, item in enumerate(note_template.keys()):
                current_note[item] = note[n]
            notes.append(current_note.copy())
    print(notes)
    return notes


#Функция записывает новую заметку в файл. В случае успеха возвращает True; если запись не выполнена - возвращает False
def save_note(new_note):
    tmp = []
    for key in new_note:
        tmp.append(str(new_note[key]))
    tmp = ','.join(tmp)

    try:
        with open("notes.txt", "a", encoding='utf-8') as f:
            f.write(tmp + '\n')
            print("Заметка успешно создана")
            return True
    except:
        print("Ошибка записи")
        return False


#Функция принимает в качестве аргументов список словарей и id нужного словаря. Словарь с этим id удаляет из списка.
def del_note(selected_id):
    readed_notes = get_notes()
    for ind, note in enumerate(readed_notes):
        if note["id"] == selected_id:
            deleted_note = readed_notes.pop(ind)
            save_all(readed_notes)
            break
    return deleted_note


#Функция принимает в качестве аргументов список словарей и отредактированный словарь. Заменяет в списке в искомом
#словаре "title" и "text" на новые. При этом обновляется "date_update". Возвращается отредактированный список словарей.
def replace_not(new_note):
    readed_notes = get_notes()
    for note in readed_notes:
        if new_note["id"] == note["id"]:
            note["title"] = new_note["title"]
            note["text"] = new_note["text"]
            note["date_update"] = str(int(time.time()))
            break
    print("Note list: ", readed_notes)
    save_all(readed_notes)
    return readed_notes


#Принимает в качестве аргумента список словарей и записывает из в файл
def save_all(notes_to_save):
    with open("notes.txt", "w", encoding="utf-8") as f:
        for ind, note in enumerate(notes_to_save):
            tmp = []
            for key in note:
                tmp.append(note[key])
            f.write(','.join(tmp) + '\n')


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
        save_note(recieved_date)

    # Показать имеющиеся заметки
    if recieved_date["id"] == "" and recieved_date["title"] == "":
        notes = get_notes()
        data = json.dumps(notes).encode()
        conn.sendall(data)

    # Удалить заметку
    if recieved_date["id"] != "" and recieved_date["title"] == "":
        print("Here is ok")
        del_note(recieved_date["id"])

    # Изменить заметку
    if recieved_date["id"] != "" and recieved_date["title"] != "" and recieved_date["text"] != "":
        print("recieved date - ", recieved_date)
        print("Edit here")
        print("replaced note list", replace_not(new_note=recieved_date))
