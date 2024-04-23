class Szoba:
    def __init__(self, ar: int, szobaszam: int):
        self.ar = ar
        self.szobaszam = szobaszam

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam: int):
        super().__init__(100, szobaszam)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam: int):
        super().__init__(200, szobaszam)

class Foglalas:
    ev = None
    honap = None
    nap = None

    def __init__(self, szoba: Szoba, erkezes: str, tavozas: str):
        self.szoba = szoba
        self.erkezes = self.datumFormazas(erkezes)
        self.tavozas = self.datumFormazas(tavozas)

    def datumFormazas(self, datum: str):
        datum = datum.split(".")
        
        if len(datum) != 3:
            return False
        
        return {'ev': datum[0], 'honap': datum[1].rjust(2, "0"), 'nap': datum[2].rjust(2, "0")}

class Szalloda:
    def __init__(self):
        self.nev = "Gazdag ember Szálloda"
        self.szobak = dict()
        self.foglalasok = dict()
        
        self.szobakFeltoltese()
        
        print("Szobák:", self.szobak)
    
    def szobakFeltoltese(self):
        for i in range(1, 6):
            self.szobaHozzaadas(EgyagyasSzoba(100 + i))
        
        for i in range(6, 11):
            self.szobaHozzaadas(KetagyasSzoba(200 + i - 6))

    def szobaHozzaadas(self, szoba: Szoba):
        self.szobak[szoba.szobaszam] = szoba.ar

    def szobaLefoglalas(self, adat: Foglalas):
        self.foglalasok[adat.szoba.szobaszam] = {'erkezes': adat.erkezes, 'tavozas': adat.tavozas}
    
        print("Lefoglalt szobák:", self.foglalasok)
    
        return adat.szoba.ar
        
szalloda = Szalloda()
szalloda.szobaLefoglalas(Foglalas(EgyagyasSzoba(101), "2024.04.23", "2024.04.25"))
szalloda.szobaLefoglalas(Foglalas(KetagyasSzoba(205), "2024.05.12", "2024.06.01"))