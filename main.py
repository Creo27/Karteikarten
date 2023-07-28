import customtkinter as ct
import sqlite3
import random

# Fenster wird erstellt
ct.set_appearance_mode("dark")  # Modes: system (default), light, dark
ct.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
root = ct.CTk()
root.geometry("1000x620")
root.title("Karteikarten")
root.resizable(False, False)

# Verbidung mit der Datenbank
conn = sqlite3.connect("Karteikarten.db")
cursor = conn.cursor()
seen_flashcards = []
def erstellen(): # erster Tab "Erstellen/Ändern"
    # Widgets werden entfernt
    t3.place_forget()
    b7.place_forget()
    b8.place_forget()
    b9.place_forget()
    l3.place_forget()
    l4.place_forget()
    l5.place_forget()
    l6.place_forget()

    # Widgets werden platziert
    l1.place(x=470, y=190)
    l2.place(x=480, y=320)
    t1.place(x=380, y=220)
    t2.place(x=25, y=350)
    karten.place(x=450, y=120)
    b4.place(x=310, y=560)
    b5.place(x=460, y=560)
    b6.place(x=610, y=560)

def lernen(): # zweiter Tab "Lernen"
    l1.place_forget()
    t1.place_forget()
    l2.place_forget()
    t2.place_forget()
    karten.place_forget()
    b4.place_forget()
    b5.place_forget()
    b6.place_forget()
    l5.place_forget()
    l6.place_forget()

    l3.place(x=400, y=480)
    b7.place(x=450, y=380)

    cursor.execute("SELECT COUNT(*) FROM Karten")
    total_flashcards = cursor.fetchone()[0]

    l3.configure(text="Karteikarten gelernt: {} von {}".format(len(seen_flashcards), total_flashcards))

    next_random_card()
def delete(): # Funktion um Karten zu löschen
    vorderseite = t1.get("1.0", ct.END).strip()

    cursor.execute("SELECT Kartennummer, Vorderseite FROM Karten WHERE LOWER(Vorderseite) = LOWER(?)", (vorderseite,))
    result = cursor.fetchone()
    kartennummer = result[0]

    cursor.execute("DELETE FROM Karten WHERE Kartennummer=?", (kartennummer,))
    conn.commit()

    delete_label = ct.CTkLabel(root, text="Gelöscht!", font=("Arial", 16))
    delete_label.place(x=700, y=180)

    root.after(2000, delete_label.place_forget)

    t1.delete("1.0", ct.END)
    t2.delete("1.0", ct.END)

def edit():
    vorderseite = t1.get("1.0", ct.END).strip()
    rueckseite = t2.get("1.0", ct.END).strip()

    cursor.execute("UPDATE Karten SET Rueckseite=?, Vorderseite=? WHERE Kartennummer=?", (rueckseite, vorderseite, id))
    conn.commit()

    edit_label = ct.CTkLabel(root, text="Geändert!", font=("Arial", 16))
    edit_label.place(x=700, y=180)

    root.after(2000, edit_label.place_forget)

    t1.delete("1.0", ct.END)
    t2.delete("1.0", ct.END)

def add():
    vorderseite = t1.get("1.0", ct.END).strip()
    rueckseite = t2.get("1.0", ct.END)

    if not vorderseite or not rueckseite:
        error_label = ct.CTkLabel(root, text="Fehler: Bitte die Vorder- und Rückseite eingeben!", font=("Arial", 16),)
        error_label.place(x=630, y=180)
        root.after(3000, error_label.place_forget)
        return

    cursor.execute("INSERT INTO Karten (Vorderseite, Rueckseite) VALUES (?, ?)", (vorderseite, rueckseite))
    cursor.execute("SELECT Kartennummer FROM Karten WHERE Vorderseite=?", (vorderseite,))
    conn.commit()

    t1.delete("1.0", ct.END)
    t2.delete("1.0", ct.END)

    kartennummer_label = ct.CTkLabel(root, text="Erstellt!", font=("Arial", 16))
    kartennummer_label.place(x=700, y=180)
    root.after(2000, kartennummer_label.place_forget)

    t1.delete("1.0", ct.END)
    t2.delete("1.0", ct.END)

    values.clear()
    cursor.execute("SELECT Vorderseite FROM Karten")
    result = cursor.fetchall()
    for item in result:
        values.append(item[0])

    karten['values'] = values

def callback(wahl):
    cursor.execute("SELECT Rueckseite FROM Karten WHERE Vorderseite=?", (wahl,))
    result = cursor.fetchone()

    if result:
        rueckseite = result[0]
        t1.delete("1.0", ct.END)
        t1.insert(ct.END, wahl)

        t2.delete("1.0", ct.END)
        t2.insert(ct.END, rueckseite)
    else:
        t1.delete("1.0", ct.END)
        t2.delete("1.0", ct.END)

    cursor.execute("SELECT Kartennummer FROM Karten WHERE Vorderseite=?", (wahl,))
    result = cursor.fetchone()
    global id
    id = result[0]

def umdrehen():
    l1.place_forget()
    b7.place_forget()
    l5.place_forget()
    l5.place_forget()
    l6.place_forget()

    l6.place(x=500, y=100, anchor='center')
    b8.place(x=330, y=380)
    b9.place(x=520, y=380)

    cursor.execute("SELECT Rueckseite FROM Karten WHERE Kartennummer=?", (id2,))
    back_side = cursor.fetchone()[0]
    formatted_text = add_line_breaks(back_side)
    add_line_breaks(formatted_text)
    l6.configure(text=formatted_text)
def wusste():
    l1.place_forget()
    t1.place_forget()
    l2.place_forget()
    t2.place_forget()
    karten.place_forget()
    b4.place_forget()
    b5.place_forget()
    b6.place_forget()
    b8.place_forget()
    b9.place_forget()
    l6.place_forget()

    l3.place(x=400, y=480)
    b7.place(x=450, y=380)

    seen_flashcards.append(id2)
    cursor.execute("SELECT COUNT(*) FROM Karten")
    total_flashcards = cursor.fetchone()[0]

    l3.configure(text="Karteikarten gelernt: {} von {}".format(len(seen_flashcards), total_flashcards))

    if len(seen_flashcards) < total_flashcards:
        next_random_card()
    else:
        l1.place_forget()
        t1.place_forget()
        l2.place_forget()
        t2.place_forget()
        l5.place_forget()
        l6.place_forget()
        karten.place_forget()
        b4.place_forget()
        b5.place_forget()
        b6.place_forget()
        b7.place_forget()
        b8.place_forget()
        b9.place_forget()
        l4.place(x=410, y=280)
def wusste_nicht():
    l1.place_forget()
    t1.place_forget()
    l2.place_forget()
    t2.place_forget()
    l5.place_forget()
    l6.place_forget()
    karten.place_forget()
    b4.place_forget()
    b5.place_forget()
    b6.place_forget()
    b8.place_forget()
    b9.place_forget()
    next_random_card()

def add_line_breaks(text):
    words = text.split()
    lines = [words[i:i+14] for i in range(0, len(words), 14)]
    return '\n'.join(' '.join(line) for line in lines)
def next_random_card():
    l3.place(x=400, y=480)

    l5.place(x=500, y=100, anchor='center')
    b7.place(x=450, y=380)

    global seen_flashcards

    cursor.execute("SELECT Kartennummer, Vorderseite FROM Karten WHERE Kartennummer NOT IN ({})".format(','.join(map(str, seen_flashcards))))
    result = cursor.fetchall()
    random_card = random.choice(result)
    kartennummer, vorderseite = random_card

    formatted_text = add_line_breaks(vorderseite)
    add_line_breaks(formatted_text)
    l5.configure(text=formatted_text)

    cursor.execute("SELECT Kartennummer FROM Karten WHERE Vorderseite=?", (vorderseite,))
    result = cursor.fetchone()

    global id2
    id2 = result[0]

values=[]

cursor.execute("SELECT Vorderseite FROM Karten")
result = cursor.fetchall()
for item in result:
    values.append(item[0])

karten = ct.CTkComboBox(root, command=callback, values=values, state="readonly")

b1 = ct.CTkButton(root, text="Erstellen/ändern", font=("Arial", 16), command=erstellen)
b1.place(x=370, y=30)
b2 = ct.CTkButton(root, text="Lernen", font=("Arial", 16), command=lernen)
b2.place(x=520, y=30)

l1 = ct.CTkLabel(root, text="Vorderseite", font=("Arial", 20))
t1 = ct.CTkTextbox(root, width=300, height=80)
l2 = ct.CTkLabel(root, text="Rückseite", font=("Arial", 20))
t2 = ct.CTkTextbox(root, width=950)

b4 = ct.CTkButton(root, text="Neu erstellen", font=("Arial", 16), command=add)
b5 = ct.CTkButton(root, text="Löschen", font=("Arial", 16), command=delete)
b6 = ct.CTkButton(root, text="Ändern", font=("Arial", 16), command=edit)
b7 = ct.CTkButton(root, text="Umdrehen", font=("Arial", 16), command=umdrehen)
t3 = ct.CTkTextbox(root, width=850, height=400)

l3 = ct.CTkLabel(root, text="Gelernte Karteikarten: ", font=("Arial", 20))
b8 = ct.CTkButton(root, text="Ich wusste die Antwort", font=("Arial", 16), command=wusste)
b9 = ct.CTkButton(root, text="Ich wusste die Antwort nicht", command=wusste_nicht, font=("Arial", 16))
l4 = ct.CTkLabel(root, text="Alle Karteikarten gelernt!", font=("Arial", 20))
l5 = ct.CTkLabel(root, text="", font=("Arial", 20))
l6 = ct.CTkLabel(root, text="", font=("Arial", 20))

root.mainloop()
