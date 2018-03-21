#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import json

import Classes
import Functions


#Функция принимает заданные аршументы (незаданные остаются по дефолту) и формирует строку для передаяи по сети,
#переводя в json и кодируя
def server_request(uuid_note="", title="", text="", date_create=0000000000, date_update=0000000000):
    send_data = {"id": uuid_note, "title": title, "text": text, "date_create": date_create, "date_update": date_update}
    data = json.dumps(send_data).encode()
    sock.send(data)

    recieved_data = sock.recv(1024)
    return json.loads(recieved_data.decode("utf-8"))


def print_all(data_to_print):
    id_list = []
    if len(data_to_print) == 0:
        print("База пуста")
    else:
        for ind, readed_note in enumerate(data_to_print):
            print("\n", ind + 1, ". Заголовок:      ", readed_note["title"])
            print("     Текст заметки:  ", readed_note["text"])
            print("     Дата создания:  ", time.ctime(int(readed_note["date_create"])))
            print("     Дата изменения: ", time.ctime(int(readed_note["date_update"])))
            id_list.append(readed_note["id"])
    return id_list


sock = socket.socket()
sock.connect(('localhost', 8080))
print("Соединение установлено")

choosen_mode = ''

while choosen_mode != 'q':
    choosen_mode = input("""
Выберите действие
    1. Создать заметку
    2. Получить все заметки
    3. Удалить заметку
    4. Редактировать заметку
    (Для завершения работы программы введите "q")
    -> """)

    if len(choosen_mode) == 1 and choosen_mode.isdigit():
        #Создание заметки
        if choosen_mode == "1":
            title_input = ""
            text_input = ""
            while len(title_input) > 30 or len(title_input) == 0:
                title_input = input("\nВведите заголовок заметки"
                                    "\n(Длина заголовка должна быть не более 30 символов)\n -> ")
                if len(title_input) > 30:
                    print("Ошибка ввода. Попробуйте ещё раз\n")
            while len(text_input) > 500 or len(text_input) == 0:
                text_input = input("\nВведите текст заметки"
                                   "\n(Длина заметки не должна превышать 500 символов)\n -> ")
                if len(text_input) > 500:
                    print("Ошибка ввода. Попробуйте ещё раз\n")

            answer = server_request(title=title_input, text=text_input)
            if answer["title"] == title_input and answer["text"] == text_input and answer["id"] != "":
                print("\nЗаметка успешно создана")
            else:
                print("Ошибка записи")

        elif choosen_mode == "2":
            print_all(server_request())

        elif choosen_mode == "3":
            id_list = print_all(server_request())
            select_note = int(input("\nУкажите номер заметки для удаления -> "))
            while not select_note in range(len(id_list) + 1):
                print("Введенный номер выходит за границы диапозона")
                select_note = int(input("\nУкажите номер заметки для удаления -> "))
            answer = server_request(uuid_note=id_list[select_note-1])
            if answer["id"] == id_list[select_note-1]:
                print("Удаление прошло успешно")

        elif choosen_mode == "4":
            id_list = print_all(server_request())
            select_note = int(input("\nУкажите номер заметки для редактирования -> "))
            while not select_note in range(len(id_list) + 1):
                print("Введенный номер выходит за границы диапозона")
                select_note = int(input("\nУкажите номер заметки для редактирования -> "))

            new_title = ''
            new_text = ''
            while len(new_title) > 30 or len(new_title) == 0:
                new_title = input("\nВведите заголовок заметки"
                                    "\n(Длина заголовка должна быть не более 30 символов)\n -> ")
                if len(new_title) > 30:
                    print("Ошибка ввода. Попробуйте ещё раз\n")
            while len(new_text) > 500 or len(new_text) == 0:
                new_text = input("\nВведите текст заметки"
                                   "\n(Длина заметки не должна превышать 500 символов)\n -> ")
                if len(new_text) > 500:
                    print("Ошибка ввода. Попробуйте ещё раз\n")
            answer = server_request(uuid_note=id_list[select_note-1], title=new_title, text=new_text)
            if answer["title"] == new_title and answer["text"] == new_text:
                print("Заметка успешно отредактирована")
            else:
                print("Новая заметка не сохранена")
        else:
            pass
    else:
        print("Некорректный ввод")


sock.close()