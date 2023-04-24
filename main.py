import math
from math import pi, cos, sin, sqrt
from typing import Tuple
import random as rd
from random import random
import numpy as np
from matplotlib import pyplot as plt

kwantyzacja = []
kwantyzacja.clear()
suma_nieaktywnych_neuronow = []


def get_random_point(center: Tuple[float, float], radius: float) -> Tuple[float, float]:
    shift_x, shift_y = center

    a = random() * 2 * pi
    r = radius * sqrt(random())

    return r * cos(a) + shift_x, r * sin(a) + shift_y


def losowanie_punktow(ilosc, x_srodka, y_srodka, promien):
    lista_x_y = []
    lista_punktow = []

    for i in range(0, ilosc):
        lista_x_y.append(get_random_point((x_srodka, y_srodka), promien))
        lista_punktow.append(Punkt(lista_x_y[i][0], lista_x_y[i][1], i))

    return lista_punktow


class Punkt:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

    def getId(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y


def srednia(lista):
    return sum(lista) / len(lista)


def wariancja(lista):
    wariancja = 0
    for i in lista:
        wariancja += (i - srednia(lista)) ** 2
    return wariancja / len(lista)


def odchylenie_standardowe(lista):
    return wariancja(lista) ** (1 / 2)


def odleglosc_punktu_od_centra(punkt_treningowy, centroid):
    return (abs(punkt_treningowy.getX() - centroid.getX()) ** 2 + abs(
        punkt_treningowy.getY() - centroid.getY()) ** 2) ** (1 / 2)


def posortowana_lista_centroid(punkt_treningowy, lista_centroid):
    lista_centroid.sort(key=lambda c: odleglosc_punktu_od_centra(punkt_treningowy, c))


def ruch_centroidy(centroid, punkt_treningowy, indeks, parametr_alfa, parametr_lambda):
    centroid.setX(centroid.getX() + parametr_alfa * math.exp(-indeks / (2 * parametr_lambda)) * (
                punkt_treningowy.getX() - centroid.getX()))
    centroid.setY(centroid.getY() + parametr_alfa * math.exp(-indeks / (2 * parametr_lambda)) * (
                punkt_treningowy.getY() - centroid.getY()))


def punkt_centroida(punkt, centroida):
    return punkt, centroida


def losuj_kolor(centroid):
    random_color = list(np.random.choice(range(10000), size=3))
    random_color[0] /= 10000
    random_color[1] /= 10000
    random_color[2] /= 10000
    return centroid, random_color


def rysuj(lista_punkt_centroida, lista_kolorow, epoka):
    for k in range(0, len(lista_kolorow)):
        plt.scatter(lista_kolorow[k][0].getX(), lista_kolorow[k][0].getY(), color=lista_kolorow[k][1])
    for p in range(0, len(lista_punkt_centroida)):
        for c in range(0, len(lista_kolorow)):
            if (lista_punkt_centroida[p][1] == lista_kolorow[c][0]):
                plt.scatter(lista_punkt_centroida[p][0].getX(), lista_punkt_centroida[p][0].getY(),
                            color=lista_kolorow[c][1], s=10)
    plt.title("Epoka " + str(epoka))
    plt.show()


def liczba_nieaktywnych_centroid(poczatkowa_lista_centroid, koncowa_lista_centroid):
    licznik = 0
    for i in poczatkowa_lista_centroid:
        for j in koncowa_lista_centroid:
            if (i.getId() == j.getId()):
                if (odleglosc_punktu_od_centra(i, j) <= 0.001):
                    licznik += 1
    return licznik


def kopia_lista_punktow(lista_punktow):
    lista_obiektow = []
    for i in lista_punktow:
        lista_obiektow.append(Punkt(i.getX(), i.getY(), i.getId()))
    return lista_obiektow


def gaz_neuronowy_wykresy(lista_punktow, lista_centroid, ilosc_epok, parametr_alfa, parametr_lambda):
    lista_punkt_centroida = []
    lista_kolorow = []
    blad_kwantyzacji = []
    poczatkowa_lista_centroid = kopia_lista_punktow(lista_centroid)
    for c in range(0, len(lista_centroid)):
        lista_kolorow.append(losuj_kolor(lista_centroid[c]))
    for p in lista_punktow:
        posortowana_lista_centroid(p, lista_centroid)
        lista_punkt_centroida.append(punkt_centroida(p, lista_centroid[0]))
    # rysuj(lista_punkt_centroida, lista_kolorow, 0)
    for i in range(0, ilosc_epok):
        lista_punkt_centroida.clear()
        for p in lista_punktow:
            posortowana_lista_centroid(p, lista_centroid)
            lista_punkt_centroida.append(punkt_centroida(p, lista_centroid[0]))
        # rysuj(lista_punkt_centroida, lista_kolorow, i+1)
        error = 0
        tym_punkty = lista_punktow.copy()
        for p in range(0, len(lista_punktow)):
            losowa = rd.randint(0, len(tym_punkty) - 1)
            tym_punkt = tym_punkty[losowa]
            posortowana_lista_centroid(tym_punkt, lista_centroid)
            for c in range(0, len(lista_centroid)):
                ruch_centroidy(lista_centroid[c], tym_punkt, c, parametr_alfa, parametr_lambda)
            posortowana_lista_centroid(tym_punkt, lista_centroid)
            error += odleglosc_punktu_od_centra(tym_punkt, lista_centroid[0])
            tym_punkty.pop(losowa)
            blad_kwantyzacji.append(error / len(lista_punktow))
    suma_nieaktywnych_neuronow.append(liczba_nieaktywnych_centroid(poczatkowa_lista_centroid, lista_centroid))
    kwantyzacja.append(srednia(blad_kwantyzacji))


def rysuj_wykres_bl_kwantyzacji(lista):
    plt.plot(lista, kwantyzacja, color='blue')
    kwantyzacja.clear()
    plt.xlabel('Liczba Centroid')
    plt.ylabel('Błąd kwantyzacji')
    plt.show()


# gaz_neuronowy_wykresy(losowanie_punktow(100, 3, 0, 0.5) + losowanie_punktow(100, -3, 0, 0.5),
#                       losowanie_punktow(20, 0, 0, 2), 20, 0.4, 0.2)
# gaz_neuronowy_wykresy(losowanie_punktow(200, 0, 0, 1), losowanie_punktow(20, 0, 0, 2), 10, 0.4, 0.2)
#
# lista = (2, 4, 6, 8, 10, 12, 14, 16, 18, 20)
# for a in lista:
#     gaz_neuronowy_wykresy(losowanie_punktow(200, 0, 0, 2), losowanie_punktow(a, 0, 0, 4), 20, 0.9, 0.2)
# rysuj_wykres_bl_kwantyzacji(lista)
# for a in lista:
#     gaz_neuronowy_wykresy(losowanie_punktow(100, 3, 0, 1) + losowanie_punktow(100, -3, 0, 1),
#                           losowanie_punktow(a, 0, 0, 4), 20, 0.9, 0.2)
# rysuj_wykres_bl_kwantyzacji(lista)

lista_2 = (0.1, 0.3, 0.5, 0.7, 0.9)
for a in lista_2:
    suma_nieaktywnych_neuronow.clear()
    kwantyzacja.clear()
    for i in range(0, 100):
        gaz_neuronowy_wykresy(losowanie_punktow(200, 0, 0, 2), losowanie_punktow(20, 0, 0, 4), 20, a, 0.2)
        # gaz_neuronowy_wykresy(losowanie_punktow(100, 3, 0, 1) + losowanie_punktow(100, -3, 0, 1), losowanie_punktow(20, 0, 0, 4), 20, a, 0.2)
    print("Średni błąd kwantyzacji: ")
    print(srednia(kwantyzacja))
    print("Odchylenie standardowe: ")
    print(odchylenie_standardowe(kwantyzacja))
    print("Minimalny błąd kwantyzacji: ")
    print(min(kwantyzacja))
    print("Średnia liczba nieaktywnych neuronów: ")
    print(srednia(suma_nieaktywnych_neuronow))
    print("Odchylenie od średniaj liczby nieaktywnych neuronów: ")
    print(odchylenie_standardowe(suma_nieaktywnych_neuronow))
