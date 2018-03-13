import socket
import json

import Classes
import Funcions


def get_notes_from_db():
    id_list =  []
    sock.send(Funcions.send_note())
    data = sock.recv(1024).decode()
    data = json.loads(data)

    for ind, readed_note in enumerate(data):
        id_list.append(readed_note["id"])
        print(ind + 1, ". Заголовок:    ", readed_note["title"])
        print("    Текст заметки:", readed_note["text"], "\n")
    return id_list


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
        if choosen_mode == 1:
            title_input = input("Введите заголовок заметки")
            text_input = input("Введите текст заметки")

            sock.send(Funcions.send_note(title=title_input, text=text_input))
            print("Заметка успешно создана")

        elif choosen_mode == 2:
            get_notes_from_db()

        elif choosen_mode == 3:
            id_list = get_notes_from_db()
            print(id_list)

            select_note = int(input("Укажите номер заметки для удаления - "))
            sock.send(Funcions.send_note(id=id_list[select_note-1]))

        elif choosen_mode == 4:
            pass
        else:
            pass
    else:
        print("Некорректный ввод")

# if data:
#     sock.send(data.encode())
#     data = sock.recv(1024)
#     udata = json.loads(data.decode("utf-8"))
#     print("Data is: ", udata)
input()

# while True:
#     # data = input("Введите послание")
#     data = json.dumps(note)
#     if data:
#         sock.send(data.encode())
#         data = sock.recv(1024)
#         # udata = data.decode()
#         udata = json.loads(data.decode("utf-8"))
#         print("Data is: ", data)
#         # data = ""

sock.close()