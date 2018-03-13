import json
import socket
import Classes


note_template = {
    "id": "",
    "title": "",
    "text": "",
    "date_create": 0,
    "date_update": 0
}


def save_note(new_note):
    tmp = []
    for key in new_note:
        tmp.append(str(new_note[key]))
    tmp = ','.join(tmp)

    try:
        with open("notes.txt", "a") as f:
            f.write('\n' + tmp)
    except:
        print(new_note)
        with open("notes.txt", "a", encoding='utf-8') as f:
            f.write('\n' + tmp)

    return True


def get_notes():
    notes = []
    current_note = {}
    with open("notes.txt", encoding='utf-8') as f:
        for note in f:
            note = note.strip().split(',')
            for n, item in enumerate(note_template.keys()):
                current_note[item] = note[n]
            notes.append(current_note.copy())
    return notes


def send_note(id="", title="", text="", date_create=0000000000, date_update=0000000000):
    send_data = {"id": id, "title": title, "text": text, "date_create": date_create, "date_update": date_update}
    data = json.dumps(send_data).encode()
    # socket.socket().send(data)
    return data
    # try:
    #     socket.socket().send(data)
    #     return True
    # except:
    #     print("Ошибка")
    #     return False


def recieve_note(host, address):
    data = b""
    while not b"\r\n" in data:
        tmp = host.recv(1024)
        if not data:
            break
        else:
            data += tmp
    return json.loads(data.decode("utf-8"))
