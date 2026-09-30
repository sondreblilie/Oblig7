from datetime import datetime
import csv

DATO_FORMATER = ["%d.%m.%Y", "%d %m %Y", "%d-%m-%Y", "%d%m%Y"]

def skriv_inn_dato_v2():
# Innså i ettertid at oppgaven ikke ville ha en dato, men et årstall, så denne er ubrukelig
    while True:
        dato_input = input("Skriv inn en dato (DD.MM.YYYY): ").strip()
        for frmt in DATO_FORMATER:
            try:
                dato = datetime.strptime(dato_input, frmt)
                break
            except ValueError:
                dato = None

        if dato is not None:
            return dato.strftime("%d.%m.%Y")
        
        print("\nUgyldig dato. Datoen må være i ett av følgende format:"
                "\n\nDD.MM.YYYY"
                "\nDD-MM-YYYY"
                "\nDD MM YYYY"
                "\nDDMMYYYY"
                "\n")

def skriv_inn_årstall():
    while True:
        dato_input = input("Skriv inn et årstall (YYYY):").strip()
        try:
            dato = datetime.strptime(dato_input, "%Y")
            return dato.strftime("%Y")
        except ValueError:
            print("Årstallet må ha fire siffer.")
            continue