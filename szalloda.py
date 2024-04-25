from datetime import datetime, date
from random import randint, choice

class Szoba:
    def __init__(self, szobaszam: int, ar: int):
        self.szobaszam = szobaszam
        self.ar = ar

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam: int, ar: int = 100):
        super().__init__(szobaszam, ar)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam: int, ar: int = 100):
        super().__init__(szobaszam, ar)

class Foglalas:
    ev = None
    honap = None
    nap = None

    def __init__(self, szoba: Szoba, erkezes: str, tavozas: str):
        self.szoba = szoba
        self.erkezes = datetime.strptime(erkezes, '%Y.%m.%d').timestamp()
        self.tavozas = datetime.strptime(tavozas, '%Y.%m.%d').timestamp()

class Szalloda:
    def __init__(self, szobamennyiseg: int, elorefoglalt: int):
        self.nev = "Gazdag ember"
        self.datum = date.today().strftime('%Y.%m.%d')
        self.ma = datetime.strptime(self.datum, '%Y.%m.%d').timestamp()
        
        self.szobak = dict()
        self.foglalasok = []
        
        if szobamennyiseg:
            self.szobakFeltoltese(szobamennyiseg)
        
        if elorefoglalt:
            self.szobakLefoglalasa(elorefoglalt)
    
    def szobakFeltoltese(self, mennyiseg: int):
        for _ in range(0, mennyiseg):
            egyagyas = bool(randint(0, 1))
            ar = 150 if egyagyas else 250
            
            if egyagyas:
                self.szobaHozzaadas(EgyagyasSzoba(randint(100, 199), ar))
            else:
                self.szobaHozzaadas(KetagyasSzoba(randint(200, 299), ar))

    def szobaHozzaadas(self, szoba: Szoba):
        self.szobak[szoba.szobaszam] = {'ár': szoba.ar, 'típus': 'egyágyas' if isinstance(szoba, EgyagyasSzoba) else 'kétágyas'}

    def elerhetoIdoszak(self, szobaszam: int, erkezes: int, tavozas: int):
        if szobaszam not in self.szobak:
            print(f"Nincsen {szobaszam} számú szoba!")
            return False
        
        if erkezes == tavozas:
            print(f"A(z) {szobaszam} számú foglaláson azonos érkezési és távozási nap van megadva!")
            return False
        
        if erkezes > tavozas:
            print(f"A(z) {szobaszam} számú foglaláson az érkezési dátum később van, mint a távozási dátum!")
            return False

        if erkezes < self.ma or tavozas < self.ma:
            print(f"A(z) {szobaszam} számú foglalás nem lehetséges, mivel nem tudsz időt utazni!")
            return False
        
        if szobaszam in self.foglalasok:
            foglalas = self.foglalasok.get(szobaszam)
            fErkezes = foglalas.get('erkezes')
            fTavozas = foglalas.get('tavozas')

            if erkezes <= fTavozas and tavozas >= fErkezes:
                print(f"A(z) {szobaszam} számú szoba ekkor már FOGLALT!")
                return False

        return True

    def szobakLefoglalasa(self, mennyiseg: int):
        for _ in range(0, mennyiseg):
            szobaszam = choice(list(self.szobak.keys()))

            erkezes = [randint(2024, 2028), randint(6, 12), randint(1, 23)]
            tavozas = [erkezes[0], erkezes[1], erkezes[2] + randint(1, 7)]

            erkezes = f"{erkezes[0]}.{str(erkezes[1]).rjust(2, '0')}.{str(erkezes[2]).rjust(2, '0')}"
            tavozas = f"{tavozas[0]}.{str(tavozas[1]).rjust(2, '0')}.{str(tavozas[2]).rjust(2, '0')}"

            self.szobaLefoglalas(Foglalas(Szoba(szobaszam, 0), erkezes, tavozas), False)
    
    def szobaLefoglalas(self, adat: Foglalas, visszajelzes: bool = True):
        szobaszam = adat.szoba.szobaszam
        erkezes = adat.erkezes
        tavozas = adat.tavozas
        
        if not self.elerhetoIdoszak(szobaszam, erkezes, tavozas):
            return

        self.foglalasok.append({'szobaszam': szobaszam, 'erkezes': erkezes , 'tavozas': tavozas})
    
        erkezes = datetime.fromtimestamp(erkezes).strftime('%Y.%m.%d')
        tavozas = datetime.fromtimestamp(tavozas).strftime('%Y.%m.%d')

        if visszajelzes:
            print(f"Sikeres foglalás a {szobaszam} számú szobára {erkezes} és {tavozas} között!")
        return adat.szoba.ar
    
    def foglalasLemondas(self, szobaszam: int, erkezes: str, tavozas: str):
        erkezes = datetime.strptime(erkezes, '%Y.%m.%d').timestamp()
        tavozas = datetime.strptime(tavozas, '%Y.%m.%d').timestamp()

        for foglalas in self.foglalasok:
            fszobaszam = foglalas['szobaszam']
            ferkezes = foglalas['erkezes']
            ftavozas = foglalas['tavozas']

            if fszobaszam == szobaszam and ferkezes == erkezes and ftavozas == tavozas:
                self.foglalasok.remove(foglalas)
                print(f"A {szobaszam} számú szoba foglalása {datetime.fromtimestamp(erkezes).strftime('%Y.%m.%d')} - {datetime.fromtimestamp(tavozas).strftime('%Y.%m.%d')} között sikeresen törölve!")
                return

        print(f"A {szobaszam} számú szoba foglalása {datetime.fromtimestamp(erkezes).strftime('%Y.%m.%d')} - {datetime.fromtimestamp(tavozas).strftime('%Y.%m.%d')} között nem található!")
    
    def foglalasokListazasa(self):
        print(f"A(z) {szalloda.nev} szálloda foglalásainak listája:")
        
        for foglalas in self.foglalasok:
            print(f"A {foglalas['szobaszam']} szoba le van foglalva {datetime.fromtimestamp(foglalas['erkezes']).strftime('%Y.%m.%d')} - {datetime.fromtimestamp(foglalas['tavozas']).strftime('%Y.%m.%d')} között")


#Felhasználói Interfész
class Porta:
    def __init__(self, szalloda = Szalloda):
        self.szallodaPorta()
        
    def szobakListazasa(self):
        print(f"\nA(z) {szalloda.nev} szálloda szobáinak listája:")

        for szobaszam, szoba in szalloda.szobak.items():
            print(f"{szobaszam} - {szoba['típus']} szoba, ára: {szoba['ár']} Ft")

    def szallodaPorta(self):
        print(f"Üdvözölöm a {szalloda.nev} szállódában, miben segíthetek?")

        while True:
            print()
            print("1 - Szoba foglalás")
            print("2 - Szoba lemondás")
            print("3 - Foglalások listázása")
            print("4 - Szobák listázása")
            print("5 - Kilépés")
            
            try:
                valasz = input("Válassz a menüpontok közül: ")
            except KeyboardInterrupt:
                print("\nElhagytad a portát.")
                break
            
            if valasz == "1":
                try:
                    szobaszam = int(input(f"Add meg a szoba számát: "))
                except ValueError:
                    print("Csak számot adhatsz meg!")
                    continue
                except KeyboardInterrupt:
                    print("\nElhagytad a portát.")
                    break
                
                try:
                    erkezes = input("Add meg az érkezésed dátumát (pl.: 2024.04.24): ")
                except KeyboardInterrupt:
                    print("\nElhagytad a portát.")
                    break
                
                if self.datumellenorzes(erkezes) == False:
                    print("Hibás dátum formátum!")
                    continue

                try:
                    tavozas = input("Add meg a távozásod dátumát (pl.: 2024.04.25): ")
                except KeyboardInterrupt:
                    print("\nElhagytad a portát.")
                    break
                
                if self.datumellenorzes(tavozas) == False:
                    print("Hibás dátum formátum!")
                    continue

                szalloda.szobaLefoglalas(Foglalas(Szoba(szobaszam, 0), erkezes, tavozas))

            elif valasz == "2":
                try:
                    szobaszam = int(input("Add meg a szoba számát: "))
                except ValueError:
                    print("Csak számot adhatsz meg!")
                    continue
                except KeyboardInterrupt:
                    print("\nElhagytad a portát.")
                    break
                
                try:
                    erkezes = input("Add meg az érkezési dátumot (pl.: 2024.04.24): ")
                except KeyboardInterrupt:
                    print("\nElhagytad a portát.")
                    break
                
                if self.datumellenorzes(erkezes) == False:
                    print("Hibás dátum formátum!")
                    continue
                
                try:
                    tavozas = input("Add meg a távozási dátumot (pl.: 2024.04.25): ")
                except KeyboardInterrupt:
                    print("\nElhagytad a portát.")
                    break
                
                if self.datumellenorzes(tavozas) == False:
                    print("Hibás dátum formátum!")
                    continue
                
                szalloda.foglalasLemondas(szobaszam, erkezes, tavozas)

            elif valasz == "3":
                szalloda.foglalasokListazasa()

            elif valasz == "4":
                self.szobakListazasa()

            elif valasz == "5":
                print("Viszont látásra!")
                break

    def datumellenorzes(self, datum: str):
        try:
            datetime.strptime(datum, '%Y.%m.%d')
            return True
        except ValueError:
            return False

szalloda = Szalloda(szobamennyiseg = 3, elorefoglalt = 5)
porta = Porta(szalloda)
