from tkinter import *
import tkintermapview

import psycopg2
from folder.controller import remove_user, update_user

pracownicy: list = []
uczelnie: list = []
import requests
from bs4 import BeautifulSoup

aktualny_mode = 'Pracownicy'

class Pracownik:
    def __init__(self, name: str,nazwisko: str, lokalizacja_uczelni: str,nazwa_uczelni: str,  wydzial: str):
        self.name = name
        self.nazwisko = nazwisko
        self.nazwa_uczelni = nazwa_uczelni
        self.wydzial = wydzial
        self.lokalizacja_uczelni = lokalizacja_uczelni
        self.coords = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name)

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url: str = f'https://pl.wikipedia.org/wiki/{self.lokalizacja_uczelni}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        # print(response.text)
        response_html = BeautifulSoup(response.text, 'html.parser')
        # print(response_html.prettify())

        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        # print(latitude)
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        # print(longitude)
        return [latitude, longitude]

def add_user(users_data:list)->None:
    name:str = entry_name.get()
    nazwisko: str = entry_nazwisko.get()
    nazwa_uczelni:str = entry_nazwa_uczelni.get()
    wydzial:str = entry_wydzial.get()
    lokalizacja:str = entry_lokalizacja_uczelni.get()
    users_data.append(Pracownik(name=name, lokalizacja_uczelni=lokalizacja, nazwisko=nazwisko, nazwa_uczelni=nazwa_uczelni, wydzial=wydzial))
    print(users_data)
    pracownik_info(users_data)
    entry_name.delete(0, END)
    entry_nazwa_uczelni.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_wydzial.delete(0, END)
    entry_lokalizacja_uczelni.delete(0, END)
    entry_name.focus()


def pracownik_info (users_data_list)->None:
    list_box_lista_pracownikow.delete(0, END)
    for idx,user in enumerate(users_data_list):
        list_box_lista_pracownikow.insert(idx, f"{user.name} {user.nazwisko} {user.nazwa_uczelni} {user.wydzial} {user.lokalizacja_uczelni}")


def delete_user(users_data:list):
    i = list_box_lista_pracownikow.index(ACTIVE)
    users_data[i].marker.delete()
    users_data.pop(i)
    pracownik_info(users_data)



def edit_user(users_data:list):
    i = list_box_lista_pracownikow.index(ACTIVE)
    entry_name.insert(0, users_data[i].name)
    entry_nazwa_uczelni.insert(0, users_data[i].nazwa_uczelni)
    entry_nazwisko.insert(0, users_data[i].nazwisko)
    entry_wydzial.insert(0, users_data[i].wydzial)
    entry_lokalizacja_uczelni.insert(0, users_data[i].lokalizacja_uczelni)

    button_dodaj.config(text="Zapisz zmiany", command=lambda: update_user(users_data, i))

def update_user(users_data:list, i):
    users_data[i].name = entry_name.get()
    users_data[i].nazwa_uczelni = entry_nazwa_uczelni.get()
    users_data[i].nazwisko = entry_nazwisko.get()
    users_data[i].wydzial = entry_wydzial.get()
    users_data[i].lokalizacja_uczelni=entry_lokalizacja_uczelni.get()

    users_data[i].coords = users_data[i].get_coordinates()
    users_data[i].marker.set_position(users_data[i].coords[0], users_data[i].coords[1])
    users_data[i].marker.set_text(users_data[i].name)

    pracownik_info(users_data)

    button_dodaj.config(text="Dodaj obiekt", command=lambda: add_user(pracownicy))
    entry_name.delete(0, END)
    entry_nazwa_uczelni.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_lokalizacja_uczelni.delete(0, END)
    entry_wydzial.delete(0, END)
    entry_name.focus()

def info_uczelnie():
    list_box_lista_pracownikow.delete(0, END)
    for idx, ucz in enumerate(uczelnie):
     list_box_lista_pracownikow.insert(idx, f"{ucz['nazwa']} {ucz['miasto']} {ucz['wojewodztwo']})")

def add_uczelnie( nazwa:str, miasto:str, powiat:str, wojewodztwo:str):
    uczelnie={'nazwa': nazwa,'miasto': miasto,'powiat': powiat,'wojewodztwo': wojewodztwo}
    uczelnie.append(uczelnie)
    if aktualny_mode == 'uczelnie':
        info_uczelnie()

def switch_mode():
    global aktualny_mode
    if aktualny_mode == 'Pracownicy':
        aktualny_mode = 'uczelnie'
        button_zmien_mode.config(text='Pracownicy')
        label_lista_pracownikow.config(text='Lista Uczelni')
        info_uczelnie()
    else:
        aktualny_mode = 'Pracownicy'
        button_zmien_mode.config(text='Uczelnie')
        label_lista_pracownikow.config(text='Lista Pracowników')
        pracownik_info(pracownicy)


root = Tk()
root.title("Mapbook")
root.geometry("1450x800")
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=1)

ramka_lista_pracownikow = Frame(root)
ramka_formularz = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_pracownikow.grid(row=0, column=1, sticky="nsew")
ramka_formularz.grid(row=2, column=1, sticky="nsew")
ramka_mapa.grid(row=0, column=0, rowspan=3, sticky="nsew")

ramka_mapa.rowconfigure(0,weight=1)
ramka_mapa.columnconfigure(0,weight=1)

ramka_lista_pracownikow.columnconfigure(0, weight=1)
ramka_lista_pracownikow.rowconfigure(1, weight=1)

ramka_formularz.columnconfigure(1,weight=1)


# RAMKA_LISTA_Pracowników
label_lista_pracownikow = Label(ramka_lista_pracownikow, text="Lista Pracowników")
label_lista_pracownikow.grid(row=0, column=0, columnspan=2, sticky="w")

button_zmien_mode = Button(ramka_lista_pracownikow, text="Uczelnie", command=switch_mode)
button_zmien_mode.grid(row=0, column=2, sticky="ew")

list_box_lista_pracownikow = Listbox(ramka_lista_pracownikow)
list_box_lista_pracownikow.grid(row=1, column=0, columnspan=3, sticky="nsew")

buttom_usun = Button(ramka_lista_pracownikow, text="Usuń obiekt", command=lambda: delete_user(pracownicy))
buttom_usun.grid(row=2, column=1, sticky="ew")

buttom_edytuj_obiekt = Button(ramka_lista_pracownikow, text="Edytuj obiekt", command=lambda: edit_user(pracownicy))
buttom_edytuj_obiekt.grid(row=2, column=2, sticky="ew")


#RAMKA FORMULARZ
label_formularz = Label(ramka_formularz, text="Formularz - pracownicy ")
label_formularz.grid(row=0, column=0, columnspan=2)

label_imie = Label(ramka_formularz, text= "Imie: ")
label_imie.grid(row=1, column=0, sticky=W)

label_nazwa_uczelni = Label(ramka_formularz, text="Nazwa uczelni: ")
label_nazwa_uczelni.grid(row=3, column=0, sticky=W)

label_lokalizacja_uczelni=Label(ramka_formularz, text="Lokalizacja uczelni: ")
label_lokalizacja_uczelni.grid(row=5, column=0, sticky=W)

label_nazwisko = Label(ramka_formularz, text="Nazwisko: ")
label_nazwisko.grid(row=2, column=0, sticky=W)

label_wydzial = Label(ramka_formularz, text="Wydział: ")
label_wydzial.grid(row=4, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1, sticky="ew")

entry_nazwa_uczelni = Entry(ramka_formularz)
entry_nazwa_uczelni.grid(row=3, column=1, sticky="ew")

entry_lokalizacja_uczelni = Entry(ramka_formularz)
entry_lokalizacja_uczelni.grid(row=5, column=1, sticky="ew")

entry_nazwisko = Entry(ramka_formularz)
entry_nazwisko.grid(row=2, column=1, sticky="ew")

entry_wydzial = Entry(ramka_formularz)
entry_wydzial.grid(row=4, column=1, sticky="ew")

button_dodaj = Button(ramka_formularz, text="Dodaj obiekt", command=lambda: add_user(pracownicy))
button_dodaj.grid(row=6, column=0, columnspan=2, sticky="ew")


# RAMKA MAPY
map_widget = tkintermapview.TkinterMapView(ramka_mapa, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, sticky="nsew")

root.mainloop()

