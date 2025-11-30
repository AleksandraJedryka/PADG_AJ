import requests
from bs4 import BeautifulSoup

class User:
    def __init__(self,name:str,location:str,posts:int,img_url:str):
        self.name = name
        self.location = location
        self.posts = posts
        self.img_url = img_url
        self.coords = self.get_coordinates()

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url: str = f"https://pl.wikipedia.org/wiki/{self.location}"
        headers = {
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/122.0.0.0 Safari/537.36"
         }
        response = requests.get(url, headers=headers)
        # print(response.text)
        response_html = BeautifulSoup(response.text, "html.parser")
        # print(response_html.prettify())
        response_html.select(".latitude")
        latitude = float(response_html.select(".latitude")[1].text.replace(',', '.'))
        # print(latitude)
        longitude = float(response_html.select(".longitude")[1].text.replace(',', '.'))
        # print(longitude)
        return [latitude, longitude]

def user_info(users_data:list)->None:
    for user in users_data:
        print(f'Twój znajomy {user.name} z miejscowości {user.location} opublikował tyle {user.posts} postów ')


def add_user(users_data:list)->None:
    name:str=input("Podaj imie nowego znajomego: ")
    location:str=input("Podaj nazwe miejscowosci: ")
    posts:int=int(input("Podaj liczbę postów: "))
    img_url:str=input("Wprowadz adres url zdjęcia: ")
    users_data.append(User(name=name,location=location,posts=posts,img_url=img_url))

def remove_user(users_data:list)-> None:
        tmp_name: str = input("podaj imie użytkownika do usuniecia ze znajomych: ")
        for user in users_data:
            if user.name == tmp_name:
                users_data.remove(user)

def update_user(users_data:list)->None:
    tmp_name:str=input("podaj imie użytkownika do aktualizacji: ")
    for user in users_data:
        if user.name==tmp_name:
            user.name=input("podaj nowe imie uzytkownika: ")
            user.location=input("podaj nowa miejscowosc")
            user.posts=input("podaj liczbe postow")
            user.coords=user.get_coordinates()

def get_coordinates(city_name:str)->list:
    url:str=f"https://pl.wikipedia.org/wiki/{city_name}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36"
    }
    response=requests.get(url,headers=headers)
    #print(response.text)
    response_html=BeautifulSoup(response.text,"html.parser")
    #print(response_html.prettify())
    response_html.select(".latitude")
    latitude=float(response_html.select(".latitude")[1].text.replace(',','.'))
   # print(latitude)
    longitude=float(response_html.select(".longitude")[1].text.replace(',','.'))
   # print(longitude)
    return[latitude,longitude]
#print(get_coordinates("Wrocław"))

def get_map(users_data:list)->None:

    import folium
    m=folium.Map(location=[52.23,21.0], zoom_start=6)

    for user in users_data:

        folium.Marker(
            location=user.coords,
            tooltip="Click me!",
            popup=f"<h4>user: {user.name}</h3> {user.location} {user.posts},<img src={user.img_url}alt='1'/>",
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)

    m.save("notatnik.html")

if __name__=="__main__":
    users_data=[]
    add_user(users_data)
    remove_user(users_data)
