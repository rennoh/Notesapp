import json
import os
from datetime import datetime

Demo = False
print(f'''
      * * * Notes Application * * *

      Demo mode: {'On' if Demo else 'Off'}
      Timestamp: {datetime.now()}



      ''')
Note_faili_nimi = 'demo_notid.json' if Demo else 'notid.json'

class Notid:
    def __init__(self,Fail_nimi=Note_faili_nimi):
        self.Fail_nimi = Fail_nimi
        self.notid= []
        self.next_id = 1
        self.loe_notid()
        Viimati_muudetud_aeg = datetime.now()

    # Failidega tegelemine
    
    def loe_notid(self):
        if not os.path.exists(self.Fail_nimi):
            self.notid = []
            self.next_id = 1
            return
        with open(self.Fail_nimi,'r',encoding='utf-8') as f:
            data = json.load(f)
        self.notid = data.get('Notes')
        self.next_id = data.get('next_id',1)

    # Salvesta notid faili
    def salvesta_notid(self):
        data = {
            'Notes': self.notid,
            'Next_id': self.next_id
        }
        with open(self.Fail_nimi, 'w', encoding= 'utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
            
    # Lisa uus note
    
    def lisa_note(self,title,body):
        note = {
            'id': self.next_id,
            'title': title,
            'body': body,
            'timestamp': datetime.now()
            
                }
        self.notid.append(note)
        self.next_id += 1
        self.salvesta_notid()
        return note
    
    # Muuda note-i 


    
    # Kustuta note id järgi

    def kustuta_note(self,note_id):
        self.notid = [note for note in self.notid if note['id'] != note_id]
        self.salvesta_notid()
    
    # Listi kõik notid

    def noti_list(self):
        return[{'id': note['id'], 'title': note['title'], 'timestamp': note['timestamp']} for note in self.notid]
 

# DEMO KONSOOLI INTERFACIGA KASUTAJA VAADE
def main():
    manager = Notid()
    while True:
        print('''
              * * * Notesapp * * *
              1. Listi notid)
              ''')
        valik = input('Valik:')
        
        if valik not in ['1','2','3','4']:
            print('Valik pole kehtiv, proovi uuesti.')
        elif valik == '1':
            notid = manager.noti_list()
            for note in notid:
                print(f'{note['title']}, Muudetud: {note['timestamp']} ')
            


                
        

if __name__ == "__main__":
    main()