
tmp = '[1, 2, 3, 4, 5]'
print(tmp)
tmp = tmp.split(',')
print(tmp)

def del_note(notes, selected_id):
    for ind, note in enumerate(notes):
        if note["id"] == selected_id:
            notes.pop(ind)
            break