from tkinter import *
import tkintermapview

import psycopg2
from folder.controller import remove_user, update_user

pracownicy: list = []
uczelnie: list = []
studenci: list = []
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

def info_studenci():
    list_box_lista_pracownikow.delete(0, END)
    for idx, st in enumerate(studenci):
        list_box_lista_pracownikow.insert(idx, f"{st['imie']}")

def show_pracownicy_form():
            label_imie.grid()
            entry_name.grid()
            label_nazwisko.grid()
            entry_nazwisko.grid()
            label_nazwa_uczelni.grid()
            entry_nazwa_uczelni.grid()
            label_wydzial.grid()
            entry_wydzial.grid()
            label_lokalizacja_uczelni.grid()
            entry_lokalizacja_uczelni.grid()
            try:
                label_ucz_nazwa.grid_remove()
                entry_ucz_nazwa.grid_remove()
                label_ucz_miasto.grid_remove()
                entry_ucz_miasto.grid_remove()
                label_ucz_powiat.grid_remove()
                entry_ucz_powiat.grid_remove()
                label_ucz_wojew.grid_remove()
                entry_ucz_wojew.grid_remove()
            except NameError:
                pass

def show_uczelnie_form():
    label_imie.grid_remove()
    entry_name.grid_remove()
    label_nazwisko.grid_remove()
    entry_nazwisko.grid_remove()
    label_nazwa_uczelni.grid_remove()
    entry_nazwa_uczelni.grid_remove()
    label_wydzial.grid_remove()
    entry_wydzial.grid_remove()
    label_lokalizacja_uczelni.grid_remove()
    entry_lokalizacja_uczelni.grid_remove()
    label_ucz_nazwa.grid(row=1, column=0, sticky=W)
    entry_ucz_nazwa.grid(row=1, column=1, sticky="ew")
    label_ucz_miasto.grid(row=2, column=0, sticky=W)
    entry_ucz_miasto.grid(row=2, column=1, sticky="ew")
    label_ucz_powiat.grid(row=3, column=0, sticky=W)
    entry_ucz_powiat.grid(row=3, column=1, sticky="ew")
    label_ucz_wojew.grid(row=4, column=0, sticky=W)
    entry_ucz_wojew.grid(row=4, column=1, sticky="ew")



def add_uczelnie():
    nazwa = entry_ucz_nazwa.get()
    miasto = entry_ucz_miasto.get()
    powiat = entry_ucz_powiat.get()
    wojewodztwo = entry_ucz_wojew.get()
    ucz = {'nazwa': nazwa, 'miasto': miasto, 'powiat': powiat, 'wojewodztwo': wojewodztwo}
    uczelnie.append(ucz)
    if aktualny_mode == 'uczelnie':
        info_uczelnie()
    entry_ucz_nazwa.delete(0, END)
    entry_ucz_miasto.delete(0, END)
    entry_ucz_powiat.delete(0, END)
    entry_ucz_wojew.delete(0, END)
    entry_ucz_nazwa.focus()

def update_uczelnia(i):
    uczelnie[i]['nazwa'] = entry_ucz_nazwa.get()
    uczelnie[i]['miasto'] = entry_ucz_miasto.get()
    uczelnie[i]['powiat'] = entry_ucz_powiat.get()
    uczelnie[i]['wojewodztwo'] = entry_ucz_wojew.get()
    info_uczelnie()
    button_dodaj.config(text="Dodaj obiekt", command=lambda: add_user(pracownicy) if aktualny_mode == 'Pracownicy' else add_uczelnie())
    entry_ucz_nazwa.delete(0, END)
    entry_ucz_miasto.delete(0, END)
    entry_ucz_powiat.delete(0, END)
    entry_ucz_wojew.delete(0, END)
    entry_ucz_nazwa.focus()

def delete_current():
    i = list_box_lista_pracownikow.index(ACTIVE)
    if aktualny_mode == 'Pracownicy':
        pracownicy[i].marker.delete()
        pracownicy.pop(i)
        pracownik_info(pracownicy)
    elif aktualny_mode == 'uczelnie':
        uczelnie.pop(i)
        info_uczelnie()
    elif aktualny_mode == 'studenci':
        studenci.pop(i)
        info_studenci()

def edit_current():
    i = list_box_lista_pracownikow.index(ACTIVE)
    if aktualny_mode == 'Pracownicy':
        edit_user(pracownicy)
    elif aktualny_mode == 'uczelnie':
        entry_ucz_nazwa.delete(0, END)
        entry_ucz_miasto.delete(0, END)
        entry_ucz_powiat.delete(0, END)
        entry_ucz_wojew.delete(0, END)
        entry_ucz_nazwa.insert(0, uczelnie[i]['nazwa'])
        entry_ucz_miasto.insert(0, uczelnie[i]['miasto'])
        entry_ucz_powiat.insert(0, uczelnie[i]['powiat'])
        entry_ucz_wojew.insert(0, uczelnie[i]['wojewodztwo'])
        button_dodaj.config(text="Zapisz zmiany", command=lambda idx=i: update_uczelnia(idx))

def set_mode(mode:str):
    global aktualny_mode
    aktualny_mode = mode
    if mode == 'uczelnie':
        label_lista_pracownikow.config(text='Lista Uczelni')
        label_formularz.config(text='Formularz - uczelnie ')
        show_uczelnie_form()
        button_dodaj.config(text="Dodaj obiekt", command=add_uczelnie)
        info_uczelnie()
    elif mode == 'studenci':
        label_lista_pracownikow.config(text='Lista Studenci')
        label_formularz.config(text='Formularz - studenci ')
        info_studenci()
    else:
        label_lista_pracownikow.config(text='Lista Pracowników')
        label_formularz.config(text='Formularz - pracownicy ')
        show_pracownicy_form()
        button_dodaj.config(text="Dodaj obiekt", command=lambda: add_user(pracownicy))
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
label_lista_pracownikow.grid(row=0, column=0, columnspan=2, sticky="ew")

button_zmien_mode = Button(ramka_lista_pracownikow, text="Uczelnie", command=lambda: set_mode('uczelnie'))
button_zmien_mode.grid(row=0, column=2, sticky="ew")

button_zmien_mode_pracownicy = Button(ramka_lista_pracownikow, text="Pracownicy", command=lambda: set_mode('Pracownicy'))
button_zmien_mode_pracownicy.grid(row=0, column=3, sticky="ew")

button_zmien_mode_studenci = Button(ramka_lista_pracownikow, text="Studenci", command=lambda: set_mode('studenci'))
button_zmien_mode_studenci.grid(row=0, column=4, sticky="ew")

list_box_lista_pracownikow = Listbox(ramka_lista_pracownikow)
list_box_lista_pracownikow.grid(row=1, column=0, columnspan=5, sticky="nsew")

buttom_usun = Button(ramka_lista_pracownikow, text="Usuń obiekt", command=lambda: delete_user(pracownicy))
buttom_usun.grid(row=2, column=3, sticky="ew")

buttom_edytuj_obiekt = Button(ramka_lista_pracownikow, text="Edytuj obiekt", command=lambda: edit_user(pracownicy))
buttom_edytuj_obiekt.grid(row=2, column=4, sticky="ew")


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

label_ucz_nazwa = Label(ramka_formularz, text="Nazwa: ")
entry_ucz_nazwa = Entry(ramka_formularz)

label_ucz_miasto = Label(ramka_formularz, text="Miasto: ")
entry_ucz_miasto = Entry(ramka_formularz)

label_ucz_powiat = Label(ramka_formularz, text="Powiat: ")
entry_ucz_powiat = Entry(ramka_formularz)

label_ucz_wojew = Label(ramka_formularz, text="Wojewodztwo: ")
entry_ucz_wojew = Entry(ramka_formularz)

button_dodaj = Button(ramka_formularz, text="Dodaj obiekt", command=lambda: add_user(pracownicy))
button_dodaj.grid(row=6, column=0, columnspan=2, sticky="ew")

show_pracownicy_form()

# RAMKA MAPY
map_widget = tkintermapview.TkinterMapView(ramka_mapa, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, sticky="nsew")

root.mainloop()

