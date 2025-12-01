from tkinter import *
import tkintermapview

import psycopg2
from folder.controller import remove_user, update_user
db_engine = psycopg2.connect(
        user="postgres",
        database="projekt_padg",
        password="postgres",
        port="5432",
        host="localhost"
)

users: list = []
uczelnie: list = []
import requests
from bs4 import BeautifulSoup

current_mode = 'obiekty'

class User:
    def __init__(self, name: str, location: str, posts: int, img_url: str):
        self.name = name
        self.location = location
        self.posts = posts
        self.img_url = img_url
        self.coords = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name)

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
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

def add_user(users_data:list, db_engine=db_engine)->None:
    cursor = db_engine.cursor()
    name:str = entry_name.get()
    location:str = entry_lokalizacja.get()
    posts:int = int(entry_posty.get())
    img_url:str = entry_img_url.get()
    user=User(name=name, location=location, posts=posts, img_url=img_url)
    users_data.append(User(name=name, location=location, posts=posts, img_url=img_url))
    print(users_data)
    sql = f"INSERT INTO public.userss(name,location, posts, img_url, geometry) VALUES ('{name}', '{location}', {posts}, '{img_url}', 'SRID=4326;POINT({user.coords[0]} {user.coords[1]})');"
    user_info(users_data)
    entry_name.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_posty.delete(0, END)
    entry_img_url.delete(0, END)
    entry_name.focus()

    cursor.execute(sql)
    db_engine.commit()


def user_info (users_data_list,db_engine=db_engine)->None:
    list_box_lista_obiektow.delete(0, END)
    sql = "SELECT *, ST_AsEWKT(geometry) FROM public.userss"
    cursor = db_engine.cursor()
    cursor.execute(sql)
    users_data = cursor.fetchall()
    users_data_list=users_data
    # print(list(map(float, user[-1][16:-1].split())))


    for idx,user in enumerate(users_data_list):
        list_box_lista_obiektow.insert(idx, f"{user[1]} {user[2]} {user[3]}" )


def delete_user(users_data:list):
    i = list_box_lista_obiektow.index(ACTIVE)
    users_data[i].marker.delete()
    users_data.pop(i)
    user_info(users_data)

def user_details(users_data:list):
    i = list_box_lista_obiektow.index(ACTIVE)
    label_imie_szczegoly_obiektu_wartosc.config(text=users_data[i][1])
    label_lokalizacja_szczegoly_obiektu_wartosc.config(text=users_data[i][2])
    label_posty_szczegoly_obiektu_wartosc.config(text=users_data[i][3])
    tmp_coords=(list(map(float,users_data[i][-1][16:-1].split())))
    map_widget.set_position(tmp_coords[0], tmp_coords[1])
    map_widget.set_zoom(14)

def edit_user(users_data:list):
    i = list_box_lista_obiektow.index(ACTIVE)
    entry_name.insert(0, users_data[i].name)
    entry_lokalizacja.insert(0, users_data[i].location)
    entry_posty.insert(0, users_data[i].posts)
    entry_img_url.insert(0, users_data[i].img_url)

    button_dodaj_obiekt.config(text="Zapisz zmiany",command=lambda: update_user(users_data,i))

def update_user(users_data:list, i):
    users_data[i].name = entry_name.get()
    users_data[i].location = entry_lokalizacja.get()
    users_data[i].posts = entry_posty.get()
    users_data[i].img_url = entry_img_url.get()

    users_data[i].coords = users_data[i].get_coordinates()
    users_data[i].marker.set_position(users_data[i].coords[0], users_data[i].coords[1])
    users_data[i].marker.set_text(users_data[i].name)

    user_info(users_data)

    button_dodaj_obiekt.config(text="Dodaj obiekt", command=lambda: add_user(users))
    entry_name.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_posty.delete(0, END)
    entry_img_url.delete(0, END)
    entry_name.focus()

def display_uczelnie():
    list_box_lista_obiektow.delete(0, END)
    for idx, ucz in enumerate(uczelnie):
     list_box_lista_obiektow.insert(idx, f"{ucz['nazwa']} {ucz['miasto']} {ucz['wojewodztwo']})")

def add_uczelnie( nazwa:str, miasto:str, powiat:str, wojewodztwo:str):
    uczelnie={'nazwa': nazwa,'miasto': miasto,'powiat': powiat,'wojewodztwo': wojewodztwo}
    uczelnie.append(uczelnie)
    if current_mode == 'uczelnie':
        display_uczelnie()

def switch_mode():
    global current_mode
    if current_mode == 'obiekty':
        current_mode = 'uczelnie'
        button_zmien_mode.config(text='Obiekty')
        label_lista_obiektow.config(text='Lista Uczelni')
        display_uczelnie()
    else:
        current_mode ='obiekty'
        button_zmien_mode.config(text='Uczelnie')
        label_lista_obiektow.config(text='Lista Obiektów')
        user_info(users)


root = Tk()
root.title("Mapbook")
root.geometry("1450x800")
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=1)

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektu = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=1, sticky="nsew")
ramka_formularz.grid(row=2, column=1, sticky="nsew")
ramka_szczegoly_obiektu.grid(row=1, column=1, sticky="ew")
ramka_mapa.grid(row=0, column=0, rowspan=3, sticky="nsew")

ramka_mapa.rowconfigure(0,weight=1)
ramka_mapa.columnconfigure(0,weight=1)

ramka_lista_obiektow.columnconfigure(0,weight=1)
ramka_lista_obiektow.rowconfigure(1,weight=1)

ramka_formularz.columnconfigure(1,weight=1)

ramka_szczegoly_obiektu.columnconfigure(1,weight=1)
ramka_szczegoly_obiektu.columnconfigure(4,weight=1)

# RAMKA_LISTA_OBIEKTÓW
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista obiektów")
label_lista_obiektow.grid(row=0, column=0, columnspan=2, sticky="w")

button_zmien_mode = Button(ramka_lista_obiektow, text="Uczelnie", command=switch_mode)
button_zmien_mode.grid(row=0, column=2, sticky="ew")

list_box_lista_obiektow = Listbox(ramka_lista_obiektow)
list_box_lista_obiektow.grid(row=1, column=0, columnspan=3, sticky="nsew")

buttom_pokaz_szczegoly = Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=lambda: user_details(users))
buttom_pokaz_szczegoly.grid(row=2, column=0, sticky="ew")

buttom_usun_obiekt = Button(ramka_lista_obiektow, text="Usuń obiekt", command=lambda: delete_user(users))
buttom_usun_obiekt.grid(row=2, column=1, sticky="ew")

buttom_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj obiekt", command=lambda: edit_user(users))
buttom_edytuj_obiekt.grid(row=2, column=2, sticky="ew")



#RAMKA FORMULARZ
label_formularz = Label(ramka_formularz, text="Formularz ")
label_formularz.grid(row=0, column=0, columnspan=2)

label_imie = Label(ramka_formularz, text= "Imie: ")
label_imie.grid(row=1, column=0, sticky=W)

label_lokalizacja = Label(ramka_formularz, text="Lokalizacja: ")
label_lokalizacja.grid(row=2, column=0, sticky=W)

label_posty = Label(ramka_formularz, text="Posty: ")
label_posty.grid(row=3, column=0, sticky=W)

label_img_url = Label(ramka_formularz, text="Obrazek: ")
label_img_url.grid(row=4, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1, sticky="ew")

entry_lokalizacja = Entry(ramka_formularz)
entry_lokalizacja.grid(row=2, column=1, sticky="ew")

entry_posty = Entry(ramka_formularz)
entry_posty.grid(row=3, column=1, sticky="ew")

entry_img_url = Entry(ramka_formularz)
entry_img_url.grid(row=4, column=1, sticky="ew")

button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj obiekt", command=lambda: add_user(users))
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2, sticky="ew")


# RAMKA SZCZEGÓŁY OBIEKTU
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Szczegóły obiektu: ")
label_szczegoly_obiektu.grid(row=0, column=0, sticky=W)

label_imie_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text= "Imie: ")
label_imie_szczegoly_obiektu.grid(row=1, column=0)

label_imie_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1)

label_lokalizacja_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Lokalizacja: ")
label_lokalizacja_szczegoly_obiektu.grid(row=1, column=3)

label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=4)

label_posty_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text= "Posty: ")
label_posty_szczegoly_obiektu.grid(row=1, column=5)

label_posty_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="...")
label_posty_szczegoly_obiektu_wartosc.grid(row=1, column=6)


# RAMKA MAPY
map_widget = tkintermapview.TkinterMapView(ramka_mapa, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, sticky="nsew")

root.mainloop()

