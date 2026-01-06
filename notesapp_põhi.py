import json
import os
from datetime import datetime
from notesapp_gui import start_gui

Demo = False
print(f'''
      * * * NotesApp * * *
      Demo mode: {'On' if Demo else 'Off'}
      Timestamp: {datetime.now().isoformat()}
      ''')
Note_faili_nimi = 'Demo/demo.notid.json' if Demo else 'Notid/notid.json'

class Notid:
    def __init__(self,Fail_nimi=Note_faili_nimi):
        self.Fail_nimi = Fail_nimi
        self.notid= []
        self.next_id = 1
        self.loe_notid()
        Viimati_muudetud_aeg = datetime.now().isoformat()

    # Failidega tegelemine
    
    def loe_notid(self):
        if not os.path.exists(self.Fail_nimi):
            self.notid = []
            self.next_id = 1
            return
        with open(self.Fail_nimi,'r',encoding='utf-8') as f:

            data = json.load(f)
        self.notid = data.get('notes', [])
        self.next_id = data.get('next_id',1)

    # Salvesta notid faili
    
    def salvesta_notid(self):
        dirpath = os.path.dirname(self.Fail_nimi)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        data = {
            'notes': self.notid,
            'next_id': self.next_id
        }
        with open(self.Fail_nimi, 'w', encoding= 'utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    # Lisa uus note
    
    def lisa_note(self,title,body):
        note = {
            'id': self.next_id,
            'title': title,
            'body': body,
            'timestamp': datetime.now().isoformat()
            
                }
        self.notid.append(note)
        self.next_id += 1
        self.salvesta_notid()
        return note
    
    # Muuda note-i 

    def muuda_note(self, note_id, title, body, update_timestamp=True):
        """
        Muuda olemasolevat märget.
        If `update_timestamp` is False, the note's timestamp will not be modified.
        """
        for note in self.notid:
            if note['id'] == note_id:
                note['title'] = title
                note['body'] = body
                if update_timestamp:
                    note['timestamp'] = datetime.now().isoformat()
                self.salvesta_notid()
                return note
        return None
    
    def leia_note_by_id(self, note_id):
        for note in self.notid:
            if note['id'] == note_id:
                return note
    
    # Kustuta note id järgi

    def kustuta_note(self,note_id):
        self.notid = [note for note in self.notid if note['id'] != note_id]
        self.salvesta_notid()
    
    # Listi kõik notid

    def noti_list(self):
        return[{'id': note['id'], 'title': note['title'], 'timestamp': note['timestamp']} for note in self.notid]
    
# Callib GUI faili, et seda käivitada
def main():
    manager = Notid()
    start_gui(manager)

    
if __name__ == "__main__":
    main()
