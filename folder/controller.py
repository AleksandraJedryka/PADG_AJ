from tkinter import END, ACTIVE
from model import Student, Uczelnia, Pracownik

WOJEWODZTWA = [
    "Dolnośląskie", "Kujawsko-pomorskie", "Lubelskie", "Lubuskie",
    "Łódzkie", "Małopolskie", "Mazowieckie", "Opolskie",
    "Podkarpackie", "Podlaskie", "Pomorskie", "Śląskie",
    "Świętokrzyskie", "Warmińsko-mazurskie", "Wielkopolskie", "Zachodniopomorskie"
]

pracownicy: list = [
    Pracownik(imie="Jan Kowalski", lokalizacja_uczelni="Warszawa", nazwa_uczelni="Politechnika Warszawska",
              powiat="warszawski")
]
uczelnie: list = [
    Uczelnia(nazwa="Uniwersytet Jagielloński", miasto="Kraków", powiat="krakowski", wojewodztwo="Małopolskie",
             lokalizacja_uczelni="")
]
studenci: list = [
    Student(imie="Anna Nowak", nazwa_uczelni="AGH", kierunek="Informatyka", grupa_dziekanska="A1",
            lokalizacja_uczelni="Kraków", akademik="DS Alfa")
]

aktualny_mode = 'Pracownicy'

label_filter = None
combo_filter = None
map_widget = None
list_box_lista_pracownikow = None
entry_imie = None
entry_nazwa_uczelni = None
entry_powiat_prac = None
entry_lokalizacja_uczelni = None
button_dodaj = None
label_lista_pracownikow = None
label_formularz = None
label_filter_ucz = None
combo_filter_ucz = None
entry_ucz_nazwa = None
entry_ucz_miasto = None
entry_ucz_powiat = None
entry_ucz_wojew = None
entry_st_imie = None
entry_st_nazwa_uczelni = None
entry_stud_kierunek = None
entry_stud_grupa = None
entry_st_lokalizacja_uczelni = None
entry_stud_akademik = None
label_stud_kierunek = None
label_stud_grupa = None
label_stud_akademik = None
label_ucz_nazwa = None
label_ucz_miasto = None
label_ucz_powiat = None
label_ucz_wojew = None
ramka_filtry = None
label_imie = None
label_nazwa_uczelni = None
label_lokalizacja_uczelni = None
label_powiat_prac = None


def add_pracownik(users_data: list) -> None:
    imie: str = entry_imie.get()
    nazwa_uczelni: str = entry_nazwa_uczelni.get()
    powiat: str = entry_powiat_prac.get()
    lokalizacja: str = entry_lokalizacja_uczelni.get()
    pracownik = Pracownik(imie=imie, lokalizacja_uczelni=lokalizacja, nazwa_uczelni=nazwa_uczelni, powiat=powiat)
    pracownik.marker = map_widget.set_marker(pracownik.coords[0], pracownik.coords[1], text=pracownik.name)
    users_data.append(pracownik)
    print(users_data)
    pracownik_info(users_data)
    update_pracownicy_powiat_filter()
    update_pracownicy_uczelnia_filter()
    update_pracownicy_markers()
    entry_imie.delete(0, END)
    entry_nazwa_uczelni.delete(0, END)
    entry_powiat_prac.delete(0, END)
    entry_lokalizacja_uczelni.delete(0, END)
    entry_imie.focus()


def pracownik_info(users_data_list) -> None:
    list_box_lista_pracownikow.delete(0, END)
    for idx, user in enumerate(users_data_list):
        list_box_lista_pracownikow.insert(idx,
                                          f"{user.name} {user.nazwa_uczelni} {user.lokalizacja_uczelni}  {user.powiat}")


def update_pracownik(users_data: list, i):
    users_data[i].name = entry_imie.get()
    users_data[i].nazwa_uczelni = entry_nazwa_uczelni.get()
    users_data[i].powiat = entry_powiat_prac.get()
    users_data[i].lokalizacja_uczelni = entry_lokalizacja_uczelni.get()
    users_data[i].coords = users_data[i].get_coordinates()
    users_data[i].marker.set_position(users_data[i].coords[0], users_data[i].coords[1])
    users_data[i].marker.set_text(users_data[i].name)
    pracownik_info(users_data)
    update_pracownicy_powiat_filter()
    update_pracownicy_uczelnia_filter()
    update_pracownicy_markers()
    button_dodaj.config(text="Dodaj obiekt", command=lambda: add_pracownik(pracownicy))
    entry_imie.delete(0, END)
    entry_nazwa_uczelni.delete(0, END)
    entry_powiat_prac.delete(0, END)
    entry_lokalizacja_uczelni.delete(0, END)
    entry_imie.focus()


def apply_filter():
    if aktualny_mode == 'uczelnie':
        apply_uczelnie_filter()
    elif aktualny_mode == 'studenci':
        apply_studenci_filter()
    elif aktualny_mode == 'Pracownicy':
        apply_pracownicy_pow_ucz_filter()


def update_pracownicy_powiat_filter():
    if combo_filter is None:
        return
    try:
        current = combo_filter.get()
    except Exception:
        current = "Wszystkie"
    powiaty = sorted(set(p.powiat for p in pracownicy if getattr(p, 'powiat', None)))
    values = ["Wszystkie"] + powiaty
    combo_filter['values'] = values
    if current in values:
        combo_filter.set(current)
    else:
        combo_filter.set("Wszystkie")


def update_pracownicy_uczelnia_filter():
    if combo_filter_ucz is None:
        return
    try:
        current = combo_filter_ucz.get()
    except Exception:
        current = "Wszystkie"
    uczelnie_nazwy = sorted(set(p.nazwa_uczelni for p in pracownicy if getattr(p, 'nazwa_uczelni', None)))
    values = ["Wszystkie"] + uczelnie_nazwy
    combo_filter_ucz['values'] = values
    if current in values:
        combo_filter_ucz.set(current)
    else:
        combo_filter_ucz.set("Wszystkie")


def apply_pracownicy_pow_ucz_filter():
    selected_pow = combo_filter.get()
    selected_ucz = combo_filter_ucz.get() if combo_filter_ucz and combo_filter_ucz.get() else "Wszystkie"
    list_box_lista_pracownikow.delete(0, END)
    for idx, p in enumerate(pracownicy):
        if (selected_pow == "Wszystkie" or p.powiat == selected_pow) and (
                selected_ucz == "Wszystkie" or p.nazwa_uczelni == selected_ucz):
            list_box_lista_pracownikow.insert(idx, f"{p.name} {p.nazwa_uczelni} {p.powiat} {p.lokalizacja_uczelni}")
    update_pracownicy_markers(selected_pow, selected_ucz)


def update_pracownicy_markers(selected_pow=None, selected_ucz=None):
    if selected_pow is None:
        try:
            selected_pow = combo_filter.get()
        except Exception:
            selected_pow = "Wszystkie"
    if selected_ucz is None:
        try:
            selected_ucz = combo_filter_ucz.get()
        except Exception:
            selected_ucz = "Wszystkie"

    for p in pracownicy:
        try:
            matches_pow = (selected_pow == "Wszystkie" or p.powiat == selected_pow)
        except Exception:
            matches_pow = (selected_pow == "Wszystkie")
        try:
            matches_ucz = (selected_ucz == "Wszystkie" or p.nazwa_uczelni == selected_ucz)
        except Exception:
            matches_ucz = (selected_ucz == "Wszystkie")

        matches = matches_pow and matches_ucz

        if matches:
            if getattr(p, 'marker', None) is None:
                if getattr(p, 'coords', None):
                    p.marker = map_widget.set_marker(p.coords[0], p.coords[1], text=getattr(p, 'name', ''))
            else:
                try:
                    p.marker.set_position(p.coords[0], p.coords[1])
                except Exception:
                    pass
        else:
            if getattr(p, 'marker', None) is not None:
                try:
                    p.marker.delete()
                except Exception:
                    pass
                p.marker = None


def clear_all_markers():
    for p in pracownicy:
        if getattr(p, 'marker', None) is not None:
            try:
                p.marker.delete()
            except Exception:
                pass
            p.marker = None
    for u in uczelnie:
        if getattr(u, 'marker', None) is not None:
            try:
                u.marker.delete()
            except Exception:
                pass
            u.marker = None
    for s in studenci:
        if getattr(s, 'marker', None) is not None:
            try:
                s.marker.delete()
            except Exception:
                pass
            s.marker = None


def info_uczelnie():
    combo_filter['values'] = ["Wszystkie"] + WOJEWODZTWA
    combo_filter.set("Wszystkie")
    apply_uczelnie_filter()


def apply_uczelnie_filter():
    selected = combo_filter.get()
    list_box_lista_pracownikow.delete(0, END)
    for ucz in uczelnie:
        try:
            if hasattr(ucz, 'marker') and ucz.marker is not None:
                ucz.marker.delete()
        except Exception:
            pass
        ucz.marker = None

    list_idx = 0
    for ucz in uczelnie:
        if selected == "Wszystkie" or ucz.wojewodztwo == selected:
            list_box_lista_pracownikow.insert(list_idx,
                                              f"{ucz.nazwa} {ucz.miasto} {ucz.powiat} {ucz.wojewodztwo} {ucz.lokalizacja_uczelni}")
            try:
                ucz.marker = map_widget.set_marker(ucz.coords[0], ucz.coords[1], text=ucz.nazwa)
            except Exception:
                ucz.marker = None
            list_idx += 1


def info_studenci():
    apply_studenci_filter()


def apply_studenci_filter():
    selected = combo_filter.get()
    list_box_lista_pracownikow.delete(0, END)
    for idx, st in enumerate(studenci):
        if selected == "Wszystkie" or st.grupa_dziekanska == selected:
            list_box_lista_pracownikow.insert(
                idx,
                f"{st.imie} {st.nazwa_uczelni} {st.lokalizacja_uczelni} {st.kierunek} {st.grupa_dziekanska} {st.akademik}"
            )
    update_student_markers(selected)


def update_student_markers(selected=None):
    if selected is None:
        try:
            selected = combo_filter.get()
        except Exception:
            selected = "Wszystkie"

    for s in studenci:
        try:
            matches = (selected == "Wszystkie" or s.grupa_dziekanska == selected)
        except Exception:
            matches = (selected == "Wszystkie")

        if matches:
            if getattr(s, 'marker', None) is None:
                if getattr(s, 'coords', None):
                    s.marker = map_widget.set_marker(s.coords[0], s.coords[1], text=getattr(s, 'imie', ''))
            else:
                try:
                    s.marker.set_position(s.coords[0], s.coords[1])
                except Exception:
                    pass
        else:
            if getattr(s, 'marker', None) is not None:
                try:
                    s.marker.delete()
                except Exception:
                    pass
                s.marker = None


def update_student_filter():
    grupy = sorted(set(st.grupa_dziekanska for st in studenci if st.grupa_dziekanska))
    combo_filter['values'] = ["Wszystkie"] + grupy
    combo_filter.set("Wszystkie")


def show_pracownicy_form():
    label_imie.grid()
    entry_imie.grid()
    label_nazwa_uczelni.grid()
    entry_nazwa_uczelni.grid()
    label_lokalizacja_uczelni.grid()
    entry_lokalizacja_uczelni.grid()
    label_powiat_prac.grid()
    entry_powiat_prac.grid()
    label_ucz_nazwa.grid_remove()
    entry_ucz_nazwa.grid_remove()
    label_ucz_miasto.grid_remove()
    entry_ucz_miasto.grid_remove()
    label_ucz_powiat.grid_remove()
    entry_ucz_powiat.grid_remove()
    label_ucz_wojew.grid_remove()
    entry_ucz_wojew.grid_remove()
    label_stud_kierunek.grid_remove()
    entry_stud_kierunek.grid_remove()
    label_stud_grupa.grid_remove()
    entry_stud_grupa.grid_remove()
    label_stud_akademik.grid_remove()
    entry_stud_akademik.grid_remove()
    try:
        entry_st_imie.grid_remove()
        entry_st_nazwa_uczelni.grid_remove()
        entry_st_lokalizacja_uczelni.grid_remove()
    except NameError:
        pass


def show_uczelnie_form():
    label_powiat_prac.grid_remove()
    entry_powiat_prac.grid_remove()
    label_imie.grid_remove()
    entry_imie.grid_remove()
    label_nazwa_uczelni.grid_remove()
    label_lokalizacja_uczelni.grid_remove()
    entry_lokalizacja_uczelni.grid_remove()
    label_imie.grid_remove()
    entry_imie.grid_remove()
    label_nazwa_uczelni.grid_remove()
    entry_nazwa_uczelni.grid_remove()
    label_stud_kierunek.grid_remove()
    entry_stud_kierunek.grid_remove()
    label_stud_grupa.grid_remove()
    entry_stud_grupa.grid_remove()
    label_lokalizacja_uczelni.grid_remove()
    entry_lokalizacja_uczelni.grid_remove()
    label_stud_akademik.grid_remove()
    entry_stud_akademik.grid_remove()
    label_ucz_nazwa.grid()
    entry_ucz_nazwa.grid()
    label_ucz_miasto.grid()
    entry_ucz_miasto.grid()
    label_ucz_powiat.grid()
    entry_ucz_powiat.grid()
    label_ucz_wojew.grid()
    entry_ucz_wojew.grid()


def show_studenci_form():
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
    label_imie.grid_remove()
    entry_imie.grid_remove()
    label_nazwa_uczelni.grid_remove()
    entry_nazwa_uczelni.grid_remove()
    label_lokalizacja_uczelni.grid_remove()
    entry_lokalizacja_uczelni.grid_remove()
    label_imie.grid()
    entry_st_imie.grid()
    label_nazwa_uczelni.grid()
    entry_st_nazwa_uczelni.grid()
    label_stud_kierunek.grid()
    entry_stud_kierunek.grid()
    label_stud_grupa.grid()
    entry_stud_grupa.grid()
    label_lokalizacja_uczelni.grid()
    entry_st_lokalizacja_uczelni.grid()
    label_stud_akademik.grid()
    entry_stud_akademik.grid()
    button_dodaj.grid(row=9, column=0, columnspan=2, sticky="ew")


def add_student():
    student = Student(
        entry_st_imie.get(),
        entry_st_nazwa_uczelni.get(),
        entry_stud_kierunek.get(),
        entry_stud_grupa.get(),
        entry_st_lokalizacja_uczelni.get(),
        entry_stud_akademik.get()
    )
    student.marker = map_widget.set_marker(student.coords[0], student.coords[1], text=student.imie)
    studenci.append(student)
    update_student_filter()
    info_studenci()
    update_student_markers()
    entry_st_imie.delete(0, END)
    entry_st_nazwa_uczelni.delete(0, END)
    entry_stud_kierunek.delete(0, END)
    entry_stud_grupa.delete(0, END)
    entry_st_lokalizacja_uczelni.delete(0, END)
    entry_stud_akademik.delete(0, END)
    entry_st_imie.focus()


def add_uczelnie():
    nazwa = entry_ucz_nazwa.get()
    miasto = entry_ucz_miasto.get()
    powiat = entry_ucz_powiat.get()
    wojewodztwo = entry_ucz_wojew.get()
    ucz = Uczelnia(nazwa, miasto, powiat, wojewodztwo, "")
    ucz.marker = map_widget.set_marker(ucz.coords[0], ucz.coords[1], text=ucz.nazwa)
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
    studenci[i].nazwa_uczelni = entry_st_nazwa_uczelni.get()
    studenci[i].kierunek = entry_stud_kierunek.get()
    studenci[i].grupa_dziekanska = entry_stud_grupa.get()
    studenci[i].lokalizacja_uczelni = entry_st_lokalizacja_uczelni.get()
    studenci[i].akademik = entry_stud_akademik.get()
    studenci[i].coords = studenci[i].get_coordinates()
    studenci[i].marker = map_widget.set_marker(studenci[i].coords[0], studenci[i].coords[1], text=studenci[i].imie)
    update_student_filter()
    info_studenci()
    update_student_markers()
    button_dodaj.config(text="Dodaj obiekt", command=add_student)
    entry_st_imie.delete(0, END)
    entry_st_nazwa_uczelni.delete(0, END)
    entry_stud_kierunek.delete(0, END)
    entry_stud_grupa.delete(0, END)
    entry_st_lokalizacja_uczelni.delete(0, END)
    entry_stud_akademik.delete(0, END)
    entry_st_imie.focus()


def delete_current():
    i = list_box_lista_pracownikow.index(ACTIVE)
    if aktualny_mode == 'Pracownicy':
        selected_pow = combo_filter.get()
        try:
            selected_ucz = combo_filter_ucz.get()
        except Exception:
            selected_ucz = "Wszystkie"
        filtered_indices = [idx for idx, p in enumerate(pracownicy)
                            if (selected_pow == "Wszystkie" or p.powiat == selected_pow)
                            and (selected_ucz == "Wszystkie" or p.nazwa_uczelni == selected_ucz)]
        if i < len(filtered_indices):
            real_idx = filtered_indices[i]
            if getattr(pracownicy[real_idx], 'marker', None) is not None:
                try:
                    pracownicy[real_idx].marker.delete()
                except Exception:
                    pass
            pracownicy.pop(real_idx)
            pracownik_info(pracownicy)
            update_pracownicy_powiat_filter()
            update_pracownicy_uczelnia_filter()
            try:
                update_pracownicy_markers()
            except Exception:
                pass
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
        selected_pow = combo_filter.get()
        try:
            selected_ucz = combo_filter_ucz.get()
        except Exception:
            selected_ucz = "Wszystkie"
        filtered_indices = [idx for idx, p in enumerate(pracownicy)
                            if (selected_pow == "Wszystkie" or p.powiat == selected_pow)
                            and (selected_ucz == "Wszystkie" or p.nazwa_uczelni == selected_ucz)]
        if i < len(filtered_indices):
            real_idx = filtered_indices[i]
            entry_imie.delete(0, END)
            entry_nazwa_uczelni.delete(0, END)
            entry_powiat_prac.delete(0, END)
            entry_lokalizacja_uczelni.delete(0, END)
            entry_imie.insert(0, pracownicy[real_idx].name)
            entry_nazwa_uczelni.insert(0, pracownicy[real_idx].nazwa_uczelni)
            entry_powiat_prac.insert(0, pracownicy[real_idx].powiat)
            entry_lokalizacja_uczelni.insert(0, pracownicy[real_idx].lokalizacja_uczelni)
            button_dodaj.config(text="Zapisz zmiany", command=lambda idx=real_idx: update_pracownik(pracownicy, idx))
    elif aktualny_mode == 'uczelnie':
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
            entry_st_nazwa_uczelni.delete(0, END)
            entry_stud_kierunek.delete(0, END)
            entry_stud_grupa.delete(0, END)
            entry_st_lokalizacja_uczelni.delete(0, END)
            entry_stud_akademik.delete(0, END)
            entry_st_imie.insert(0, studenci[real_idx].imie)
            entry_st_nazwa_uczelni.insert(0, studenci[real_idx].nazwa_uczelni)
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
    try:
        clear_all_markers()
    except Exception:
        pass
    if mode == 'uczelnie':
        label_lista_pracownikow.config(text='Lista Uczelni')
        label_formularz.config(text='Formularz - uczelnie ')
        show_uczelnie_form()
        button_dodaj.config(text="Dodaj obiekt", command=add_uczelnie)
        label_filter.config(text="Filtruj województwo:")
        combo_filter['values'] = ["Wszystkie"] + WOJEWODZTWA
        combo_filter.set("Wszystkie")
        try:
            label_filter_ucz.grid_remove()
            combo_filter_ucz.grid_remove()
        except Exception:
            pass
        label_filter.grid(in_=ramka_filtry, row=0, column=0, sticky="w", padx=10, pady=(0, 0))
        combo_filter.grid(in_=ramka_filtry, row=0, column=1, sticky="w", padx=10, pady=(0, 0))
        info_uczelnie()
    elif mode == 'studenci':
        label_lista_pracownikow.config(text='Lista Studenci')
        label_formularz.config(text='Formularz - studenci ')
        show_studenci_form()
        button_dodaj.config(text="Dodaj obiekt", command=add_student)
        label_filter.config(text="Filtruj grupę dziekańską:")
        update_student_filter()
        combo_filter.set("Wszystkie")
        try:
            label_filter_ucz.grid_remove()
            combo_filter_ucz.grid_remove()
        except Exception:
            pass
        label_filter.grid(in_=ramka_filtry, row=0, column=0, sticky="w", padx=10, pady=(0, 0))
        combo_filter.grid(in_=ramka_filtry, row=0, column=1, sticky="w", padx=10, pady=(0, 0))
        info_studenci()
    else:
        label_lista_pracownikow.config(text='Lista Pracowników')
        label_formularz.config(text='Formularz - pracownicy ')
        show_pracownicy_form()
        button_dodaj.config(text="Dodaj obiekt", command=lambda: add_pracownik(pracownicy))
        label_filter.config(text="Filtruj powiat:")
        update_pracownicy_powiat_filter()
        update_pracownicy_uczelnia_filter()
        combo_filter_ucz.set("Wszystkie")
        label_filter_ucz.config(text="Filtruj nazwę uczelni:")
        label_filter_ucz.grid(in_=ramka_filtry, row=1, column=0, sticky="w", padx=10, pady=(5, 0))
        combo_filter_ucz.grid(in_=ramka_filtry, row=1, column=1, sticky="w", padx=10, pady=(5, 0))
        combo_filter.set("Wszystkie")
        label_filter.grid(in_=ramka_filtry, row=0, column=0, sticky="w", padx=10, pady=(0, 0))
        combo_filter.grid(in_=ramka_filtry, row=0, column=1, sticky="w", padx=10, pady=(0, 0))
        apply_pracownicy_pow_ucz_filter()
