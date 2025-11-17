import _json
import os
from datetime import datetime

Note_faili_nimi = "notid.json"

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
            data = _json.load(f)
    
