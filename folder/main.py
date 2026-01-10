from tkinter import *
from tkinter import ttk
import tkintermapview
import controller
from controller import (
    add_pracownik, pracownik_info, update_pracownik, apply_filter,
    update_pracownicy_powiat_filter, update_pracownicy_uczelnia_filter,
    apply_pracownicy_powiat_filter, update_pracownicy_markers,
    clear_all_markers, info_uczelnie, apply_uczelnie_filter,
    info_studenci, apply_studenci_filter, update_student_markers,
    update_student_filter, show_pracownicy_form, show_uczelnie_form,
    show_studenci_form, add_student, add_uczelnie, update_uczelnia,
    update_student, delete_current, edit_current, set_mode,
    pracownicy, uczelnie, studenci, aktualny_mode, WOJEWODZTWA
)

root = Tk()
root.title("Geoportal Uczelni")
root.geometry("1450x800")
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.columnconfigure(1, minsize=420)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=0)
root.rowconfigure(3, weight=1)

ramka_lista_pracownikow = Frame(root)
ramka_formularz = Frame(root)
ramka_mapa = Frame(root)
ramka_filtry = Frame(root)

ramka_lista_pracownikow.grid_propagate(False)
ramka_lista_pracownikow.configure(height=300)
ramka_filtry.grid_propagate(False)
ramka_filtry.configure(height=80)
ramka_formularz.grid_propagate(False)
ramka_formularz.configure(height=340)

ramka_lista_pracownikow.grid(row=0, column=1, sticky="nsew")
ramka_filtry.grid(row=2, column=1, sticky="nsew", padx=10, pady=(10, 0))
ramka_formularz.grid(row=3, column=1, sticky="nsew")

ramka_mapa.grid(row=0, column=0, rowspan=4, sticky="nsew")

ramka_mapa.rowconfigure(0, weight=1)
ramka_mapa.columnconfigure(0, weight=1)

ramka_lista_pracownikow.columnconfigure(0, weight=1)
ramka_lista_pracownikow.rowconfigure(1, weight=1)

ramka_formularz.columnconfigure(1, weight=1)
ramka_filtry.columnconfigure(1, weight=1)

root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=0)
root.rowconfigure(3, weight=1)

label_lista_pracownikow = Label(ramka_lista_pracownikow, text="Lista Pracowników")
label_lista_pracownikow.grid(row=0, column=0, columnspan=2, sticky="ew")

label_filter = Label(root)
combo_filter = ttk.Combobox(root, state="readonly")
combo_filter.bind("<<ComboboxSelected>>", lambda e: apply_filter())
label_filter_ucz = Label(root)
combo_filter_ucz = ttk.Combobox(root, state="readonly")
combo_filter_ucz.bind("<<ComboboxSelected>>", lambda e: apply_filter())

if aktualny_mode == 'Pracownicy':
    label_filter.config(text="Filtruj powiat:")
    update_pracownicy_powiat_filter()
    try:
        update_pracownicy_uczelnia_filter()
        label_filter_ucz.config(text="Filtruj nazwę uczelni:")
        label_filter_ucz.grid(in_=ramka_filtry, row=1, column=0, sticky="w", padx=10, pady=(5, 0))
        combo_filter_ucz.grid(in_=ramka_filtry, row=1, column=1, sticky="w", padx=10, pady=(5, 0))
    except Exception:
        pass
elif aktualny_mode == 'uczelnie':
    label_filter.config(text="Filtruj województwo:")
    combo_filter['values'] = ["Wszystkie"] + WOJEWODZTWA
    combo_filter.set("Wszystkie")
elif aktualny_mode == 'studenci':
    label_filter.config(text="Filtruj grupę dziekańską:")
    update_student_filter()

label_filter.grid(in_=ramka_filtry, row=0, column=0, sticky="w", padx=10, pady=(0, 0))
combo_filter.grid(in_=ramka_filtry, row=0, column=1, sticky="w", padx=10, pady=(0, 0))

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

label_formularz = Label(ramka_formularz, text="Formularz - pracownicy ")
label_formularz.grid(row=0, column=0, columnspan=2)

label_imie = Label(ramka_formularz, text="Imie: ")
label_imie.grid(row=1, column=0, sticky=W)

label_nazwa_uczelni = Label(ramka_formularz, text="Nazwa uczelni: ")
label_nazwa_uczelni.grid(row=3, column=0, sticky=W)

label_lokalizacja_uczelni = Label(ramka_formularz, text="Lokalizacja uczelni: ")
label_lokalizacja_uczelni.grid(row=5, column=0, sticky=W)

entry_imie = Entry(ramka_formularz)
entry_imie.grid(row=1, column=1, sticky="ew")

entry_nazwa_uczelni = Entry(ramka_formularz)
entry_nazwa_uczelni.grid(row=3, column=1, sticky="ew")

entry_lokalizacja_uczelni = Entry(ramka_formularz)
entry_lokalizacja_uczelni.grid(row=5, column=1, sticky="ew")

entry_st_imie = Entry(ramka_formularz)
entry_st_nazwa_uczelni = Entry(ramka_formularz)
entry_st_lokalizacja_uczelni = Entry(ramka_formularz)

label_ucz_nazwa = Label(ramka_formularz, text="Nazwa: ")
entry_ucz_nazwa = Entry(ramka_formularz)

label_ucz_miasto = Label(ramka_formularz, text="Miasto: ")
entry_ucz_miasto = Entry(ramka_formularz)

label_ucz_powiat = Label(ramka_formularz, text="Powiat: ")
entry_ucz_powiat = Entry(ramka_formularz)

label_ucz_wojew = Label(ramka_formularz, text="Wojewodztwo: ")
entry_ucz_wojew = ttk.Combobox(ramka_formularz, values=WOJEWODZTWA, state="readonly")
entry_ucz_wojew.set("")

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

map_widget = tkintermapview.TkinterMapView(ramka_mapa, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, sticky="nsew")

controller.map_widget = map_widget
controller.list_box_lista_pracownikow = list_box_lista_pracownikow
controller.entry_imie = entry_imie
controller.entry_nazwa_uczelni = entry_nazwa_uczelni
controller.entry_powiat_prac = entry_powiat_prac
controller.entry_lokalizacja_uczelni = entry_lokalizacja_uczelni
controller.button_dodaj = button_dodaj
controller.label_lista_pracownikow = label_lista_pracownikow
controller.label_formularz = label_formularz
controller.label_filter = label_filter
controller.combo_filter = combo_filter
controller.label_filter_ucz = label_filter_ucz
controller.combo_filter_ucz = combo_filter_ucz
controller.entry_ucz_nazwa = entry_ucz_nazwa
controller.entry_ucz_miasto = entry_ucz_miasto
controller.entry_ucz_powiat = entry_ucz_powiat
controller.entry_ucz_wojew = entry_ucz_wojew
controller.entry_st_imie = entry_st_imie
controller.entry_st_nazwa_uczelni = entry_st_nazwa_uczelni
controller.entry_stud_kierunek = entry_stud_kierunek
controller.entry_stud_grupa = entry_stud_grupa
controller.entry_st_lokalizacja_uczelni = entry_st_lokalizacja_uczelni
controller.entry_stud_akademik = entry_stud_akademik
controller.label_stud_kierunek = label_stud_kierunek
controller.label_stud_grupa = label_stud_grupa
controller.label_stud_akademik = label_stud_akademik
controller.label_ucz_nazwa = label_ucz_nazwa
controller.label_ucz_miasto = label_ucz_miasto
controller.label_ucz_powiat = label_ucz_powiat
controller.label_ucz_wojew = label_ucz_wojew
controller.ramka_filtry = ramka_filtry
controller.label_imie = label_imie
controller.label_nazwa_uczelni = label_nazwa_uczelni
controller.label_lokalizacja_uczelni = label_lokalizacja_uczelni
controller.label_powiat_prac = label_powiat_prac

show_pracownicy_form()

root.mainloop()
