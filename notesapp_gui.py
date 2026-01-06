import customtkinter as tk
from tkinter import Listbox, END

# GUI startimine
def start_gui(note_manager):
    theme = "dark"
    tk.set_appearance_mode(theme)

    # App-i aken
    app = tk.CTk()
    app.title("NotesApp")
    app.geometry("1280x720")

    # Notide list
    note_listbox = Listbox(app, width=20)
    note_listbox.pack(side='left', fill='y')

    right_frame = tk.CTkFrame(app)
    right_frame.pack(side='right', fill='both', expand=True)

    title_entry = tk.CTkEntry(right_frame)
    title_entry.pack(fill='x', padx=10, pady=(10,5))

    body = tk.CTkTextbox(right_frame, width=80)
    body.pack(side='top', fill='both', expand=True, padx=10, pady=(0,10))

    note_ids = []
    # Säilitame viimase valitud indeksi juhul kui Listbox kaotab valiku
    viimati_valitud_index = [-1]

    # Laeb notid listi
    def lae_notid():
        note_listbox.delete(0, END)
        note_ids.clear()
        notes = note_manager.noti_list()
        font = ("Calibri", 14)
        note_listbox.config(font=font)
        for note in notes:
            note_listbox.insert(END, note.get('title', '<no title>'))
            note_ids.append(note['id'])
        print(f"Laaditud {len(notes)} märget listi")

    # Näita kasutaja valitud noti sisu
    def kuva_valitud_note(event=None):
        valitud = note_listbox.curselection()
        if not valitud:
            return
        index = valitud[0]
        # Salvesta viimati valitud indeks
        viimati_valitud_index[0] = index
        note_id = note_ids[index]
        note = note_manager.leia_note_by_id(note_id)
        if not note:
            return
        title_entry.delete(0, END)
        title_entry.insert(0, note['title'])
        body.delete('1.0', END)
        body.insert('1.0', note['body'])

    note_listbox.bind('<<ListboxSelect>>', kuva_valitud_note)

    # Toob akna kõige ette
    app.lift()
    app.focus_force()
    app.attributes('-topmost', True)
    app.after(100, lambda: app.attributes('-topmost', False))

    lae_notid()
    if note_ids:
        note_listbox.selection_set(0)
        kuva_valitud_note()

    # Muuda noti
    def muuda_note():
        valitud = note_listbox.curselection()
        if not valitud:
            # Kui valik on tühi, kasuta viimati salvestatud indeksit
            if viimati_valitud_index[0] < 0:
                return
            index = viimati_valitud_index[0]
        else:
            index = valitud[0]
        note_id = note_ids[index]
        note = note_manager.leia_note_by_id(note_id)
        if not note:
            return
        uus_title = title_entry.get().strip()
        uus_body = body.get("1.0", END).rstrip("\n")
        if not uus_title:
            return
        note_manager.muuda_note(note_id, uus_title, uus_body)
        lae_notid()
        if note_id in note_ids:
            uus_index = note_ids.index(note_id)
            note_listbox.selection_set(uus_index)
            kuva_valitud_note()

    muuda_nupp = tk.CTkButton(app, text="Salvesta", command=muuda_note)
    muuda_nupp.pack(side='top', pady=10)

    # Loo uus note
    def loo_uus_note():
        uus_note = note_manager.lisa_note("Uus märge", "")
        lae_notid()
        if uus_note['id'] in note_ids:
            uus_index = note_ids.index(uus_note['id'])
            note_listbox.selection_set(uus_index)
            kuva_valitud_note()
    uus_nupp = tk.CTkButton(app, text="Uus märge", command=loo_uus_note)
    uus_nupp.pack(side='top', pady=10)

    # Kustuta note
    def kustuta_note():
        valitud = note_listbox.curselection()
        if not valitud:
            return
        index = valitud[0]
        note_id = note_ids[index]
        note_manager.kustuta_note(note_id)
        lae_notid()
        title_entry.delete(0, END)
        body.delete('1.0', END)
    kustuta_nupp = tk.CTkButton(app, text="Kustuta note", command=kustuta_note)
    kustuta_nupp.pack(side='top', pady=10)

    app.mainloop()
# ma vihkan GUI-de tegemist, ehitame lih koik ilusti terminal interfaciga app-e
