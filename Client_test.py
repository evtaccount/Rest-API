#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import json

import Classes
import Functions


#Функция принимает заданные аршументы (незаданные остаются по дефолту) и формирует строку для передаяи по сети,
#переводя в json и кодируя
def send_request(id="", title="", text="", date_create=0000000000, date_update=0000000000):
    send_data = {"id": id, "title": title, "text": text, "date_create": date_create, "date_update": date_update}
    data = json.dumps(send_data).encode()
    return data


def get_notes_from_db():
    exp_list = []
    sock.send(send_request())
    data = sock.recv(1024).decode()
    data = json.loads(data)

    for ind, readed_note in enumerate(data):
        print(ind + 1, ". Заголовок:      ", readed_note["title"])
        print("    Текст заметки:  ", readed_note["text"])
        print("    Дата создания:  ", time.ctime(int(readed_note["date_create"])))
        print("    Дата изменения: ", time.ctime(int(readed_note["date_update"])), "\n")
        exp_list.append(readed_note["id"])
    return exp_list


note = {
    "id": "",
    "title": "",
    "text": "",
    "date_create": 0,
    "date_update": 0
}

note_template = {
    "id": "",
    "title": "",
    "text": "",
    "date_create": 0,
    "date_update": 0
}

sock = socket.socket()
sock.connect(('localhost', 8080))
print("Соединение установлено")

while True:
    print("""Выберите действие:
    1. Создать заметку
    2. Получить все заметки
    3. Удалить заметку
    4. Редактировать заметку""")
    choosen_mode = int(input())

    if True:
        #Создание заметки
        if choosen_mode == 1:
            title_input = ""
            text_input = ""
            while len(title_input) > 30 or len(title_input) == 0:
                title_input = input("Введите заголовок заметки\nДлина заголовка должна быть не более 30 символов: ")
                if len(title_input) > 30:
                    print("Ошибка ввода. Попробуйте ещё раз\n")
            while len(text_input) > 500 or len(text_input) == 0:
                text_input = input("Введите текст заметки\nДлина заметки не должна превышать 500 символов")
                if len(text_input) > 500:
                    print("Ошибка ввода. Попробуйте ещё раз\n")

            sock.send(send_request(title=title_input, text=text_input))
            print("Заметка успешно создана")

        elif choosen_mode == 2:
            get_notes_from_db()

        elif choosen_mode == 3:
            id_list = get_notes_from_db()
            select_note = int(input("Укажите номер заметки для удаления - "))
            sock.send(send_request(id=id_list[select_note-1]))

        elif choosen_mode == 4:
            id_list = get_notes_from_db()
            print(id_list)
            select_note = int(input("Укажите номер заметки для редактирования - "))
            new_title = input("Введите новый заголовок")
            new_text = input("Введите новую заметку")
            print("id_list: ", id_list)
            sock.send(send_request(id=id_list[select_note-1], title=new_title, text=new_text))
        else:
            pass
    else:
        print("Некорректный ввод")


sock.close()