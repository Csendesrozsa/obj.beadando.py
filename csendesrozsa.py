from abc import ABC, abstractmethod
from datetime import datetime


# Osztályok létrehozása
class Szoba(ABC):
    def __init__(self, ar, szobaszam, penznem="€"):
        self.ar = ar
        self.szobaszam = szobaszam
        self.penznem = penznem

    @abstractmethod
    def szoba_tipusa(self):
        pass


class Egyagyasszoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=80, szobaszam=szobaszam)

    def szoba_tipusa(self):
        return "Egyágyas szoba"


class Ketagyasszoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=120, szobaszam=szobaszam)

    def szoba_tipusa(self):
        return "Kétágyas szoba"


# Szálloda osztály
class LindenfelsHotel:
    def __init__(self):
        self.nev = "Lindenfels Hotel"
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaadas(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        try:
            foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
            if foglalas_datum < datetime.now():
                return "A dátum nem lehet múltbeli."
        except ValueError:
            return "Érvénytelen dátum formátum."

        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                for foglalas in self.foglalasok:
                    if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                        return "A szoba már foglalt erre a dátumra."
                uj_foglalas = Foglalas(szoba, datum)
                self.foglalasok.append(uj_foglalas)
                return f"A foglalás dátuma: {datum}, Ár: {szoba.ar} {szoba.penznem}"
        return "Nincs ilyen szobaszám."

    def foglalas_lemondasa(self, szobaszam, datum):
        try:
            datetime.strptime(datum, "%Y-%m-%d")
        except ValueError:
            return "Érvénytelen dátum formátum."

        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return "Foglalás lemondva."
        return "Nem található foglalás."

    def foglalasok_listazasa(self):
        if not self.foglalasok:
            return "Nincsenek foglalások."
        return "\n".join([
            f"Szobaszám: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}, Ár: {foglalas.szoba.ar} {foglalas.szoba.penznem}"
            for foglalas in self.foglalasok])


# Foglalás osztály
class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


# Szobák és hotel létrehozása
hotel = LindenfelsHotel()
hotel.szoba_hozzaadas(Egyagyasszoba("101"))
hotel.szoba_hozzaadas(Egyagyasszoba("102"))
hotel.szoba_hozzaadas(Ketagyasszoba("201"))

# Szobák listázása a hotelben
for szoba in hotel.szobak:
    print(f"Szoba típusa: {szoba.szoba_tipusa()}, Szoba szám: {szoba.szobaszam}, Ár: {szoba.ar} {szoba.penznem}")

# Előre feltöltés foglalásokkal
hotel.foglalas("101", "2024-06-10")
hotel.foglalas("201", "2024-07-15")
hotel.foglalas("102", "2024-10-23")
hotel.foglalas("101", "2024-12-30")
hotel.foglalas("201", "2024-12-31")


def user_interface():
    print("Üdvözöljük a Lindenfels Hotel foglalási rendszerében!")
    while True:
        print("\nKérem válasszon az alábbi lehetőségek közül:")
        print("1: Szoba foglalása")
        print("2: Foglalás lemondása")
        print("3: Foglalások listázása")
        print("4: Kilépés")
        choice = input("Válassza ki a művelet számát: ")
        if choice == "1":
            szobaszam = input("Adja meg a szobaszámot: ")
            datum = input("Adja meg a foglalás dátumát (éééé-hh-nn): ")
            print(hotel.foglalas(szobaszam, datum))
        elif choice == "2":
            szobaszam = input("Adja meg a szobaszámot: ")
            datum = input("Adja meg a lemondandó foglalás dátumát (éééé-hh-nn): ")
            print(hotel.foglalas_lemondasa(szobaszam, datum))
        elif choice == "3":
            print("Aktuális foglalások:")
            print(hotel.foglalasok_listazasa())
        elif choice == "4":
            print("Kilépés a rendszerből.")
            break
        else:
            print("Érvénytelen választás. Kérem próbálja újra.")

# Program indítása
if __name__ == "__main__":
    user_interface()
