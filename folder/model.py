import requests
from bs4 import BeautifulSoup


class Student:
    def __init__(self, imie: str, nazwa_uczelni: str, kierunek: str, grupa_dziekanska: str, lokalizacja_uczelni: str, akademik: str):
        self.imie = imie
        self.nazwa_uczelni = nazwa_uczelni
        self.kierunek = kierunek
        self.grupa_dziekanska = grupa_dziekanska
        self.lokalizacja_uczelni = lokalizacja_uczelni
        self.akademik = akademik
        self.coords = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
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
        self.marker = None

    def get_coordinates(self):
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
    def __init__(self, imie: str, lokalizacja_uczelni: str, nazwa_uczelni: str, powiat: str):
        self.name = imie
        self.nazwa_uczelni = nazwa_uczelni
        self.lokalizacja_uczelni = lokalizacja_uczelni
        self.powiat = powiat
        self.coords = self.get_coordinates()
        self.marker = None

    def get_coordinates(self):
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
