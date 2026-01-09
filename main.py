class Student:
    def __init__(self, imie: str, nazwisko: str, nazwa_uczelni: str, wydzial: str, kierunek: str, grupa_dziekanska: str,
                 lokalizacja_uczelni: str, akademik: str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.nazwa_uczelni = nazwa_uczelni
        self.wydzial = wydzial
        self.kierunek = kierunek
        self.grupa_dziekanska = grupa_dziekanska
        self.lokalizacja_uczelni = lokalizacja_uczelni
        self.akademik = akademik
        self.coords = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.imie)

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
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        return [latitude, longitude]


class Uczelnia:
    def __init__(self, nazwa: str, miasto: str, powiat: str, wojewodztwo: str, lokalizacja_uczelni: str):
        self.nazwa = nazwa
        self.miasto = miasto
        self.powiat = powiat
        self.wojewodztwo = wojewodztwo
        self.lokalizacja_uczelni = lokalizacja_uczelni
        self.coords = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.nazwa)

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url: str = f'https://pl.wikipedia.org/wiki/{self.miasto}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/123.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        return [latitude, longitude]


class Pracownik:
    def __init__(self, imie: str, nazwisko: str, lokalizacja_uczelni: str, nazwa_uczelni: str, wydzial: str,
                 powiat: str):
        self.name = imie
        self.nazwisko = nazwisko
        self.nazwa_uczelni = nazwa_uczelni
        self.wydzial = wydzial
        self.lokalizacja_uczelni = lokalizacja_uczelni
        self.powiat = powiat
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


from tkinter import *
import tkintermapview

from tkinter import ttk
import psycopg2

WOJEWODZTWA = [
    "Dolnośląskie", "Kujawsko-pomorskie", "Lubelskie", "Lubuskie",
    "Łódzkie", "Małopolskie", "Mazowieckie", "Opolskie",
    "Podkarpackie", "Podlaskie", "Pomorskie", "Śląskie",
    "Świętokrzyskie", "Warmińsko-mazurskie", "Wielkopolskie", "Zachodniopomorskie"
]

pracownicy: list = []
uczelnie: list = []
studenci: list = []
import requests
from bs4 import BeautifulSoup

aktualny_mode = 'Pracownicy'

label_filter = None
combo_filter = None


def add_pracownik(users_data: list) -> None:
    imie: str = entry_imie.get()
    nazwisko: str = entry_nazwisko.get()
    nazwa_uczelni: str = entry_nazwa_uczelni.get()
    wydzial: str = entry_wydzial.get()
    powiat: str = entry_powiat_prac.get()
    lokalizacja: str = entry_lokalizacja_uczelni.get()
    users_data.append(
        Pracownik(imie=imie, lokalizacja_uczelni=lokalizacja, nazwisko=nazwisko, nazwa_uczelni=nazwa_uczelni,
                  wydzial=wydzial, powiat=powiat))
    print(users_data)
    pracownik_info(users_data)
    update_pracownicy_powiat_filter()
    entry_imie.delete(0, END)
    entry_nazwa_uczelni.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_wydzial.delete(0, END)
    entry_powiat_prac.delete(0, END)
    entry_lokalizacja_uczelni.delete(0, END)
    entry_imie.focus()


def pracownik_info(users_data_list) -> None:
    list_box_lista_pracownikow.delete(0, END)
    for idx, user in enumerate(users_data_list):
        list_box_lista_pracownikow.insert(idx,
                                          f"{user.name} {user.nazwisko} {user.nazwa_uczelni} {user.wydzial} {user.lokalizacja_uczelni}  {user.powiat}")


def update_pracownik(users_data: list, i):
    users_data[i].name = entry_imie.get()
    users_data[i].nazwa_uczelni = entry_nazwa_uczelni.get()
    users_data[i].nazwisko = entry_nazwisko.get()
    users_data[i].wydzial = entry_wydzial.get()
    users_data[i].powiat = entry_powiat_prac.get()
    users_data[i].lokalizacja_uczelni = entry_lokalizacja_uczelni.get()

    users_data[i].coords = users_data[i].get_coordinates()
    users_data[i].marker.set_position(users_data[i].coords[0], users_data[i].coords[1])
    users_data[i].marker.set_text(users_data[i].name)

    pracownik_info(users_data)
    update_pracownicy_powiat_filter()

    button_dodaj.config(text="Dodaj obiekt", command=lambda: add_pracownik(pracownicy))
    entry_imie.delete(0, END)
    entry_nazwa_uczelni.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_powiat_prac.delete(0, END)
    entry_lokalizacja_uczelni.delete(0, END)
    entry_wydzial.delete(0, END)
    entry_imie.focus()


def apply_filter():
    if aktualny_mode == 'uczelnie':
        apply_uczelnie_filter()
    elif aktualny_mode == 'studenci':
        apply_studenci_filter()
    elif aktualny_mode == 'Pracownicy':
        apply_pracownicy_powiat_filter()


def update_pracownicy_powiat_filter():
    powiaty = sorted(set(p.powiat for p in pracownicy if getattr(p, 'powiat', None)))
    combo_filter['values'] = ["Wszystkie"] + powiaty
    combo_filter.set("Wszystkie")


def apply_pracownicy_powiat_filter():
    selected = combo_filter.get()
    list_box_lista_pracownikow.delete(0, END)
    for idx, p in enumerate(pracownicy):
        if selected == "Wszystkie" or p.powiat == selected:
            list_box_lista_pracownikow.insert(idx,
                                              f"{p.name} {p.nazwisko} {p.nazwa_uczelni} {p.wydzial} {p.powiat} {p.lokalizacja_uczelni}")


def info_uczelnie():
    combo_filter['values'] = ["Wszystkie"] + WOJEWODZTWA
    combo_filter.set("Wszystkie")
    apply_uczelnie_filter()


def apply_uczelnie_filter():
    selected = combo_filter.get()
    list_box_lista_pracownikow.delete(0, END)
    for idx, ucz in enumerate(uczelnie):
        if selected == "Wszystkie" or ucz.wojewodztwo == selected:
            list_box_lista_pracownikow.insert(idx,
                                              f"{ucz.nazwa} {ucz.miasto} {ucz.powiat} {ucz.wojewodztwo} {ucz.lokalizacja_uczelni}")


def info_studenci():
    apply_studenci_filter()


def apply_studenci_filter():
    selected = combo_filter.get()
    list_box_lista_pracownikow.delete(0, END)
    for idx, st in enumerate(studenci):
        if selected == "Wszystkie" or st.grupa_dziekanska == selected:
            list_box_lista_pracownikow.insert(
                idx,
                f"{st.imie} {st.nazwisko} {st.nazwa_uczelni} {st.wydzial} {st.kierunek} {st.grupa_dziekanska} {st.lokalizacja_uczelni} {st.akademik}"
            )


def update_student_filter():
    grupy = sorted(set(st.grupa_dziekanska for st in studenci if st.grupa_dziekanska))
    combo_filter['values'] = ["Wszystkie"] + grupy
    combo_filter.set("Wszystkie")


def show_pracownicy_form():
    label_imie.grid()
    entry_imie.grid()
    label_nazwisko.grid()
    entry_nazwisko.grid()
    label_nazwa_uczelni.grid()
    entry_nazwa_uczelni.grid()
    label_wydzial.grid()
    entry_wydzial.grid()
    label_lokalizacja_uczelni.grid()
    entry_lokalizacja_uczelni.grid()
    label_powiat_prac.grid()
    entry_powiat_prac.grid()
    # Hide university fields
    label_ucz_nazwa.grid_remove()
    entry_ucz_nazwa.grid_remove()
    label_ucz_miasto.grid_remove()
    entry_ucz_miasto.grid_remove()
    label_ucz_powiat.grid_remove()
    entry_ucz_powiat.grid_remove()
    label_ucz_wojew.grid_remove()
    entry_ucz_wojew.grid_remove()
    # Hide student fields
    label_stud_kierunek.grid_remove()
    entry_stud_kierunek.grid_remove()
    label_stud_grupa.grid_remove()
    entry_stud_grupa.grid_remove()
    label_stud_akademik.grid_remove()
    entry_stud_akademik.grid_remove()
    # Hide student-specific entries
    try:
        entry_st_imie.grid_remove()
        entry_st_nazwisko.grid_remove()
        entry_st_nazwa_uczelni.grid_remove()
        entry_st_wydzial.grid_remove()
        entry_st_lokalizacja_uczelni.grid_remove()
    except NameError:
        pass


def show_uczelnie_form():
    label_powiat_prac.grid_remove()
    entry_powiat_prac.grid_remove()
    label_imie.grid_remove()
    entry_imie.grid_remove()
    label_nazwisko.grid_remove()
    entry_nazwisko.grid_remove()
    label_nazwa_uczelni.grid_remove()

    entry_wydzial.grid_remove()
    label_lokalizacja_uczelni.grid_remove()
    entry_lokalizacja_uczelni.grid_remove()
    # Hide student fields
    label_imie.grid_remove()
    entry_imie.grid_remove()
    label_nazwisko.grid_remove()
    entry_nazwisko.grid_remove()
    label_nazwa_uczelni.grid_remove()
    entry_nazwa_uczelni.grid_remove()
    label_wydzial.grid_remove()
    entry_wydzial.grid_remove()
    label_stud_kierunek.grid_remove()
    entry_stud_kierunek.grid_remove()
    label_stud_grupa.grid_remove()
    entry_stud_grupa.grid_remove()
    label_lokalizacja_uczelni.grid_remove()
    entry_lokalizacja_uczelni.grid_remove()
    label_stud_akademik.grid_remove()
    entry_stud_akademik.grid_remove()
    # Show university fields
    label_ucz_nazwa.grid()
    entry_ucz_nazwa.grid()
    label_ucz_miasto.grid()
    entry_ucz_miasto.grid()
    label_ucz_powiat.grid()
    entry_ucz_powiat.grid()
    label_ucz_wojew.grid()
    entry_ucz_wojew.grid()


def show_studenci_form():
    # Hide university fields
    label_ucz_nazwa.grid_remove()
    entry_ucz_nazwa.grid_remove()
    label_ucz_miasto.grid_remove()
    entry_ucz_miasto.grid_remove()
    label_ucz_powiat.grid_remove()
    entry_ucz_powiat.grid_remove()
    label_ucz_wojew.grid_remove()
    entry_ucz_wojew.grid_remove()

    label_powiat_prac.grid_remove()
    entry_powiat_prac.grid_remove()
    # Hide employee fields
    label_imie.grid_remove()
    entry_imie.grid_remove()
    label_nazwisko.grid_remove()
    entry_nazwisko.grid_remove()
    label_nazwa_uczelni.grid_remove()
    entry_nazwa_uczelni.grid_remove()
    label_wydzial.grid_remove()
    entry_wydzial.grid_remove()
    label_lokalizacja_uczelni.grid_remove()
    entry_lokalizacja_uczelni.grid_remove()
    # Show student fields (reuse labels, but student entries)
    label_imie.grid()
    entry_st_imie.grid(row=1, column=1, sticky="ew")
    label_nazwisko.grid()
    entry_st_nazwisko.grid(row=2, column=1, sticky="ew")
    label_nazwa_uczelni.grid()
    entry_st_nazwa_uczelni.grid(row=3, column=1, sticky="ew")
    label_wydzial.grid()
    entry_st_wydzial.grid(row=4, column=1, sticky="ew")
    label_stud_kierunek.grid()
    entry_stud_kierunek.grid(row=6, column=1, sticky="ew")
    label_stud_grupa.grid()
    entry_stud_grupa.grid(row=7, column=1, sticky="ew")
    label_lokalizacja_uczelni.grid()
    entry_st_lokalizacja_uczelni.grid(row=5, column=1, sticky="ew")
    label_stud_akademik.grid()
    entry_stud_akademik.grid(row=8, column=1, sticky="ew")
    button_dodaj.grid(row=9, column=0, columnspan=2, sticky="ew")


def add_student():
    student = Student(
        entry_st_imie.get(),
        entry_st_nazwisko.get(),
        entry_st_nazwa_uczelni.get(),
        entry_st_wydzial.get(),
        entry_stud_kierunek.get(),
        entry_stud_grupa.get(),
        entry_st_lokalizacja_uczelni.get(),
        entry_stud_akademik.get()
    )
    studenci.append(student)
    update_student_filter()
    info_studenci()
    entry_st_imie.delete(0, END)
    entry_st_nazwisko.delete(0, END)
    entry_st_nazwa_uczelni.delete(0, END)
    entry_st_wydzial.delete(0, END)
    entry_stud_kierunek.delete(0, END)
    entry_stud_grupa.delete(0, END)
    entry_st_lokalizacja_uczelni.delete(0, END)
    entry_stud_akademik.delete(0, END)
    entry_st_imie.focus()
    button_dodaj.grid(row=9, column=0, columnspan=2, sticky="ew")


def add_uczelnie():
    nazwa = entry_ucz_nazwa.get()
    miasto = entry_ucz_miasto.get()
    powiat = entry_ucz_powiat.get()
    wojewodztwo = entry_ucz_wojew.get()
    # no lokalizacja field for uczelnie; leave attribute empty
    ucz = Uczelnia(nazwa, miasto, powiat, wojewodztwo, "")
    uczelnie.append(ucz)
    if aktualny_mode == 'uczelnie':
        info_uczelnie()
    entry_ucz_nazwa.delete(0, END)
    entry_ucz_miasto.delete(0, END)
    entry_ucz_powiat.delete(0, END)
    entry_ucz_wojew.set("")

    entry_ucz_nazwa.focus()


def update_uczelnia(i):
    uczelnie[i].marker.delete()
    uczelnie[i].nazwa = entry_ucz_nazwa.get()
    uczelnie[i].miasto = entry_ucz_miasto.get()
    uczelnie[i].powiat = entry_ucz_powiat.get()
    uczelnie[i].wojewodztwo = entry_ucz_wojew.get()
    # lokalizacja_uczelni removed from form; keep existing value or empty
    uczelnie[i].coords = uczelnie[i].get_coordinates()
    uczelnie[i].marker = map_widget.set_marker(uczelnie[i].coords[0], uczelnie[i].coords[1], text=uczelnie[i].nazwa)
    info_uczelnie()
    button_dodaj.config(text="Dodaj obiekt",
                        command=lambda: add_pracownik(pracownicy) if aktualny_mode == 'Pracownicy' else add_uczelnie())
    entry_ucz_nazwa.delete(0, END)
    entry_ucz_miasto.delete(0, END)
    entry_ucz_powiat.delete(0, END)
    entry_ucz_wojew.set("")
    entry_ucz_nazwa.focus()


def update_student(i):
    studenci[i].marker.delete()
    studenci[i].imie = entry_st_imie.get()
    studenci[i].nazwisko = entry_st_nazwisko.get()
    studenci[i].nazwa_uczelni = entry_st_nazwa_uczelni.get()
    studenci[i].wydzial = entry_st_wydzial.get()
    studenci[i].kierunek = entry_stud_kierunek.get()
    studenci[i].grupa_dziekanska = entry_stud_grupa.get()
    studenci[i].lokalizacja_uczelni = entry_st_lokalizacja_uczelni.get()
    studenci[i].akademik = entry_stud_akademik.get()
    studenci[i].coords = studenci[i].get_coordinates()
    studenci[i].marker = map_widget.set_marker(studenci[i].coords[0], studenci[i].coords[1], text=studenci[i].imie)
    update_student_filter()
    info_studenci()
    button_dodaj.config(text="Dodaj obiekt", command=add_student)
    entry_st_imie.delete(0, END)
    entry_st_nazwisko.delete(0, END)
    entry_st_nazwa_uczelni.delete(0, END)
    entry_st_wydzial.delete(0, END)
    entry_stud_kierunek.delete(0, END)
    entry_stud_grupa.delete(0, END)
    entry_st_lokalizacja_uczelni.delete(0, END)
    entry_stud_akademik.delete(0, END)
    entry_st_imie.focus()


def delete_current():
    i = list_box_lista_pracownikow.index(ACTIVE)
    if aktualny_mode == 'Pracownicy':
        selected = combo_filter.get()
        filtered_indices = [idx for idx, p in enumerate(pracownicy) if selected == "Wszystkie" or p.powiat == selected]
        if i < len(filtered_indices):
            real_idx = filtered_indices[i]
            pracownicy[real_idx].marker.delete()
            pracownicy.pop(real_idx)
            pracownik_info(pracownicy)
            update_pracownicy_powiat_filter()
    elif aktualny_mode == 'uczelnie':
        selected = combo_filter.get()
        filtered_indices = [idx for idx, ucz in enumerate(uczelnie) if
                            selected == "Wszystkie" or ucz.wojewodztwo == selected]
        if i < len(filtered_indices):
            real_idx = filtered_indices[i]
            uczelnie[real_idx].marker.delete()
            uczelnie.pop(real_idx)
            info_uczelnie()
    elif aktualny_mode == 'studenci':
        selected = combo_filter.get()
        filtered_indices = [idx for idx, st in enumerate(studenci) if
                            selected == "Wszystkie" or st.grupa_dziekanska == selected]
        if i < len(filtered_indices):
            real_idx = filtered_indices[i]
            studenci[real_idx].marker.delete()
            studenci.pop(real_idx)
            update_student_filter()
            info_studenci()


def edit_current():
    i = list_box_lista_pracownikow.index(ACTIVE)
    if aktualny_mode == 'Pracownicy':
        selected = combo_filter.get()
        filtered_indices = [idx for idx, p in enumerate(pracownicy) if selected == "Wszystkie" or p.powiat == selected]
        if i < len(filtered_indices):
            real_idx = filtered_indices[i]
            entry_imie.delete(0, END)
            entry_nazwa_uczelni.delete(0, END)
            entry_nazwisko.delete(0, END)
            entry_wydzial.delete(0, END)
            entry_powiat_prac.delete(0, END)
            entry_lokalizacja_uczelni.delete(0, END)
            entry_imie.insert(0, pracownicy[real_idx].name)
            entry_nazwa_uczelni.insert(0, pracownicy[real_idx].nazwa_uczelni)
            entry_nazwisko.insert(0, pracownicy[real_idx].nazwisko)
            entry_wydzial.insert(0, pracownicy[real_idx].wydzial)
            entry_powiat_prac.insert(0, pracownicy[real_idx].powiat)
            entry_lokalizacja_uczelni.insert(0, pracownicy[real_idx].lokalizacja_uczelni)
            button_dodaj.config(text="Zapisz zmiany", command=lambda idx=real_idx: update_pracownik(pracownicy, idx))
    elif aktualny_mode == 'uczelnie':
        # Map filtered index to real index
        selected = combo_filter.get()
        filtered_indices = [idx for idx, ucz in enumerate(uczelnie) if
                            selected == "Wszystkie" or ucz.wojewodztwo == selected]
        if i < len(filtered_indices):
            real_idx = filtered_indices[i]
            entry_ucz_nazwa.delete(0, END)
            entry_ucz_miasto.delete(0, END)
            entry_ucz_powiat.delete(0, END)
            entry_ucz_wojew.set("")
            entry_ucz_nazwa.insert(0, uczelnie[real_idx].nazwa)
            entry_ucz_miasto.insert(0, uczelnie[real_idx].miasto)
            entry_ucz_powiat.insert(0, uczelnie[real_idx].powiat)
            entry_ucz_wojew.set(uczelnie[real_idx].wojewodztwo)
            button_dodaj.config(text="Zapisz zmiany", command=lambda idx=real_idx: update_uczelnia(idx))
    elif aktualny_mode == 'studenci':
        selected = combo_filter.get()
        filtered_indices = [idx for idx, st in enumerate(studenci) if
                            selected == "Wszystkie" or st.grupa_dziekanska == selected]
        if i < len(filtered_indices):
            real_idx = filtered_indices[i]
            entry_st_imie.delete(0, END)
            entry_st_nazwisko.delete(0, END)
            entry_st_nazwa_uczelni.delete(0, END)
            entry_st_wydzial.delete(0, END)
            entry_stud_kierunek.delete(0, END)
            entry_stud_grupa.delete(0, END)
            entry_st_lokalizacja_uczelni.delete(0, END)
            entry_stud_akademik.delete(0, END)
            entry_st_imie.insert(0, studenci[real_idx].imie)
            entry_st_nazwisko.insert(0, studenci[real_idx].nazwisko)
            entry_st_nazwa_uczelni.insert(0, studenci[real_idx].nazwa_uczelni)
            entry_st_wydzial.insert(0, studenci[real_idx].wydzial)
            entry_stud_kierunek.insert(0, studenci[real_idx].kierunek)
            entry_stud_grupa.insert(0, studenci[real_idx].grupa_dziekanska)
            entry_st_lokalizacja_uczelni.insert(0, studenci[real_idx].lokalizacja_uczelni)
            entry_stud_akademik.insert(0, studenci[real_idx].akademik)
            button_dodaj.config(
                text="Zapisz zmiany",
                command=lambda idx=real_idx: update_student(idx)
            )


def set_mode(mode: str):
    global aktualny_mode
    aktualny_mode = mode
    if mode == 'uczelnie':
        label_lista_pracownikow.config(text='Lista Uczelni')
        label_formularz.config(text='Formularz - uczelnie ')
        show_uczelnie_form()
        button_dodaj.config(text="Dodaj obiekt", command=add_uczelnie)
        label_filter.config(text="Filtruj województwo:")
        combo_filter['values'] = ["Wszystkie"] + WOJEWODZTWA
        combo_filter.set("Wszystkie")
        label_filter.grid(row=1, column=1, sticky="w", padx=10, pady=(10, 0))
        combo_filter.grid(row=1, column=1, sticky="e", padx=150, pady=(10, 0))
        info_uczelnie()
    elif mode == 'studenci':
        label_lista_pracownikow.config(text='Lista Studenci')
        label_formularz.config(text='Formularz - studenci ')
        show_studenci_form()
        button_dodaj.config(text="Dodaj obiekt", command=add_student)
        label_filter.config(text="Filtruj grupę dziekańską:")
        update_student_filter()
        combo_filter.set("Wszystkie")
        label_filter.grid(row=1, column=1, sticky="w", padx=10, pady=(10, 0))
        combo_filter.grid(row=1, column=1, sticky="e", padx=150, pady=(10, 0))
        info_studenci()
    else:
        label_lista_pracownikow.config(text='Lista Pracowników')
        label_formularz.config(text='Formularz - pracownicy ')
        show_pracownicy_form()
        button_dodaj.config(text="Dodaj obiekt", command=lambda: add_pracownik(pracownicy))
        label_filter.config(text="Filtruj powiat:")
        update_pracownicy_powiat_filter()
        combo_filter.set("Wszystkie")
        label_filter.grid(row=1, column=1, sticky="w", padx=10, pady=(10, 0))
        combo_filter.grid(row=1, column=1, sticky="e", padx=150, pady=(10, 0))
        apply_pracownicy_powiat_filter()


root = Tk()
root.title("Geoportal Uczelni")
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

ramka_mapa.rowconfigure(0, weight=1)
ramka_mapa.columnconfigure(0, weight=1)

ramka_lista_pracownikow.columnconfigure(0, weight=1)
ramka_lista_pracownikow.rowconfigure(1, weight=1)

ramka_formularz.columnconfigure(1, weight=1)

# Configure row weights to push the form to the bottom
root.rowconfigure(0, weight=0)  # List grows
root.rowconfigure(1, weight=0)  # Spacer fixed
root.rowconfigure(2, weight=1)  # Form stays at bottom

# RAMKA_LISTA_Pracowników

label_lista_pracownikow = Label(ramka_lista_pracownikow, text="Lista Pracowników")
label_lista_pracownikow.grid(row=0, column=0, columnspan=2, sticky="ew")

# Define filter widgets first
label_filter = Label(root)
combo_filter = ttk.Combobox(root, state="readonly")
combo_filter.bind("<<ComboboxSelected>>", lambda e: apply_filter())

# Ustaw filtr i combobox na podstawie aktualnego trybu
if aktualny_mode == 'Pracownicy':
    label_filter.config(text="Filtruj powiat:")
    update_pracownicy_powiat_filter()
elif aktualny_mode == 'uczelnie':
    label_filter.config(text="Filtruj województwo:")
    combo_filter['values'] = ["Wszystkie"] + WOJEWODZTWA
    combo_filter.set("Wszystkie")
elif aktualny_mode == 'studenci':
    label_filter.config(text="Filtruj grupę dziekańską:")
    update_student_filter()

# Now you can place them in the grid
ramka_lista_pracownikow.grid(row=0, column=1, sticky="nsew")
label_filter.grid(row=1, column=1, sticky="w", padx=10, pady=(10, 0))
combo_filter.grid(row=1, column=1, sticky="e", padx=150, pady=(10, 0))
ramka_formularz.grid(row=2, column=1, sticky="sew", padx=10, pady=10)

button_zmien_mode = Button(ramka_lista_pracownikow, text="Uczelnie", command=lambda: set_mode('uczelnie'))
button_zmien_mode.grid(row=0, column=2, sticky="ew")

button_zmien_mode_pracownicy = Button(ramka_lista_pracownikow, text="Pracownicy",
                                      command=lambda: set_mode('Pracownicy'))
button_zmien_mode_pracownicy.grid(row=0, column=3, sticky="ew")

button_zmien_mode_studenci = Button(ramka_lista_pracownikow, text="Studenci", command=lambda: set_mode('studenci'))
button_zmien_mode_studenci.grid(row=0, column=4, sticky="ew")

list_box_lista_pracownikow = Listbox(ramka_lista_pracownikow)
list_box_lista_pracownikow.grid(row=1, column=0, columnspan=5, sticky="nsew")

buttom_usun = Button(ramka_lista_pracownikow, text="Usuń obiekt", command=delete_current)
buttom_usun.grid(row=2, column=3, sticky="ew")

buttom_edytuj_obiekt = Button(ramka_lista_pracownikow, text="Edytuj obiekt", command=edit_current)
buttom_edytuj_obiekt.grid(row=2, column=4, sticky="ew")

# RAMKA FORMULARZ
label_formularz = Label(ramka_formularz, text="Formularz - pracownicy ")
label_formularz.grid(row=0, column=0, columnspan=2)

label_imie = Label(ramka_formularz, text="Imie: ")
label_imie.grid(row=1, column=0, sticky=W)

label_nazwa_uczelni = Label(ramka_formularz, text="Nazwa uczelni: ")
label_nazwa_uczelni.grid(row=3, column=0, sticky=W)

label_lokalizacja_uczelni = Label(ramka_formularz, text="Lokalizacja uczelni: ")
label_lokalizacja_uczelni.grid(row=5, column=0, sticky=W)

label_nazwisko = Label(ramka_formularz, text="Nazwisko: ")
label_nazwisko.grid(row=2, column=0, sticky=W)

label_wydzial = Label(ramka_formularz, text="Wydział: ")
label_wydzial.grid(row=4, column=0, sticky=W)

entry_imie = Entry(ramka_formularz)
entry_imie.grid(row=1, column=1, sticky="ew")

entry_nazwa_uczelni = Entry(ramka_formularz)
entry_nazwa_uczelni.grid(row=3, column=1, sticky="ew")

entry_lokalizacja_uczelni = Entry(ramka_formularz)
entry_lokalizacja_uczelni.grid(row=5, column=1, sticky="ew")

entry_nazwisko = Entry(ramka_formularz)
entry_nazwisko.grid(row=2, column=1, sticky="ew")

entry_wydzial = Entry(ramka_formularz)
entry_wydzial.grid(row=4, column=1, sticky="ew")
# Student-specific entries (separate from pracownicy)
entry_st_imie = Entry(ramka_formularz)
entry_st_nazwisko = Entry(ramka_formularz)
entry_st_nazwa_uczelni = Entry(ramka_formularz)
entry_st_wydzial = Entry(ramka_formularz)
entry_st_lokalizacja_uczelni = Entry(ramka_formularz)

label_ucz_nazwa = Label(ramka_formularz, text="Nazwa: ")
entry_ucz_nazwa = Entry(ramka_formularz)

label_ucz_miasto = Label(ramka_formularz, text="Miasto: ")
entry_ucz_miasto = Entry(ramka_formularz)

label_ucz_powiat = Label(ramka_formularz, text="Powiat: ")
entry_ucz_powiat = Entry(ramka_formularz)

label_ucz_wojew = Label(ramka_formularz, text="Wojewodztwo: ")
# Use a readonly Combobox so user picks województwo from the predefined list
entry_ucz_wojew = ttk.Combobox(ramka_formularz, values=WOJEWODZTWA, state="readonly")
entry_ucz_wojew.set("")

# lokalizacja uczelni removed from form

label_powiat_prac = Label(ramka_formularz, text="Powiat: ")
label_powiat_prac.grid(row=6, column=0, sticky=W)
entry_powiat_prac = Entry(ramka_formularz)
entry_powiat_prac.grid(row=6, column=1, sticky="ew")

label_ucz_nazwa.grid(row=1, column=0, sticky=W)
entry_ucz_nazwa.grid(row=1, column=1, sticky="ew")
label_ucz_miasto.grid(row=2, column=0, sticky=W)
entry_ucz_miasto.grid(row=2, column=1, sticky="ew")
label_ucz_powiat.grid(row=3, column=0, sticky=W)
entry_ucz_powiat.grid(row=3, column=1, sticky="ew")
label_ucz_wojew.grid(row=4, column=0, sticky=W)
entry_ucz_wojew.grid(row=4, column=1, sticky="ew")

label_stud_kierunek = Label(ramka_formularz, text="Kierunek: ")
entry_stud_kierunek = Entry(ramka_formularz)
label_stud_grupa = Label(ramka_formularz, text="Grupa dziekańska: ")
entry_stud_grupa = Entry(ramka_formularz)
label_stud_akademik = Label(ramka_formularz, text="Akademik: ")
entry_stud_akademik = Entry(ramka_formularz)

label_stud_kierunek.grid(row=6, column=0, sticky=W)
entry_stud_kierunek.grid(row=6, column=1, sticky="ew")
label_stud_grupa.grid(row=7, column=0, sticky=W)
entry_stud_grupa.grid(row=7, column=1, sticky="ew")
label_stud_akademik.grid(row=8, column=0, sticky=W)
entry_stud_akademik.grid(row=8, column=1, sticky="ew")

button_dodaj = Button(ramka_formularz, text="Dodaj obiekt", command=lambda: add_pracownik(pracownicy))
button_dodaj.grid(row=7, column=0, columnspan=2, sticky="ew")

show_pracownicy_form()

# RAMKA MAPY
map_widget = tkintermapview.TkinterMapView(ramka_mapa, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, sticky="nsew")

root.mainloop()