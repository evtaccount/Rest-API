import json
import time
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
    print(notes)
    return notes


def del_note(notes, selected_id):
    for ind, note in enumerate(notes):
        print("Wanted id ", selected_id)
        print("Current note ", note)
        if note["id"] == selected_id:
            print("Deleted note ", notes.pop(ind))
            print("Other ", notes)
            save_notes(notes)
            break


def save_notes(notes_to_save):
    with open("notes.txt", "w", encoding="utf-8") as f:
        for ind, note in enumerate(notes_to_save):
            tmp = []
            for key in note:
                tmp.append(note[key])
            f.write(','.join(tmp) + '\n')


def replace_not(note_list, new_note):
    for note in note_list:
        if new_note["id"] == note["id"]:
            note["title"] = new_note["title"]
            note["text"] = new_note["text"]
            note["date_update"] = str(int(time.time()))
            break
    print("Note list: ", note_list)
    save_notes(note_list)
    return note_list


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
