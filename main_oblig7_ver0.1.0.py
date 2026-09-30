from datetime import datetime
import csv
import sys
import matplotlib.pyplot as plt

def skriv_inn_årstall():
    while True:
        dato_input = input("Skriv inn et årstall (YYYY):").strip()
        try:
            dato = datetime.strptime(dato_input, "%Y")
            return dato.strftime("%Y")
        except ValueError:
            print("Årstallet må ha fire siffer.")
            continue

def tall(tekst):
    try:
        tallet = float(tekst.replace(",", "."))
        return tallet
    except (ValueError, AttributeError):
        tallet = float("nan")
        return tallet


dato_dict = {}
ugyldige_datoer = []

x_datoer = []
stasjon_id_liste = []
max_temp_liste = []
mid_temp_liste = []
nedbør_liste = []
høyeste_mid_vind_liste = []
snødybde_liste = []

try:
    fil = open("Obligatoriske Innleveringer/Oblig7/sinnes_2014_2025_med_makstemperatur.csv", encoding="utf-8-sig", newline="")
except FileNotFoundError:
    print("Error: Filen ble ikke funnet")
    sys.exit(1)


with fil:
    leser = csv.DictReader(fil, delimiter=";")
    
    for linje in leser:
        dato = linje.get("Tid(norsk normaltid)")
        try:
            datetime.strptime(dato, "%d.%m.%Y")
        except (ValueError, TypeError):
            ugyldige_datoer.append(dato)
            continue

        navn = linje.get("Navn")
        stasjon_id = linje.get("Stasjon")
        max_temp = linje.get("Maksimumstemperatur (døgn)")
        mid_temp = linje.get("Middeltemperatur (døgn)")
        nedbør = linje.get("Nedbør (døgn)")
        høyeste_mid_vind = linje.get("Høyeste middelvind (døgn)")
        snødybde = linje.get("Snødybde")

        dato_dict[dato] = [navn, stasjon_id, max_temp, mid_temp, nedbør, høyeste_mid_vind, snødybde]

    sortert_dict = dict(sorted(dato_dict.items(), key=lambda par: (par[0][-4:], par[0][3:5], par[0][0:2])))

    input_årstall = skriv_inn_årstall()


    for dato in sortert_dict:
        if dato[-4:] != input_årstall:
            continue
        verdier = sortert_dict[dato]
        x_datoer.append(datetime.strptime(dato, "%d.%m.%Y"))
        max_temp_liste.append(tall(verdier[2]))
        mid_temp_liste.append(tall(verdier[3]))
        nedbør_liste.append(tall(verdier[4]))
        høyeste_mid_vind_liste.append(tall(verdier[5]))
        snødybde_liste.append(tall(verdier[6]))


    plt.subplot(2, 2, 1)
    plt.plot(x_datoer, snødybde_liste)
    plt.xlabel("Dato")
    plt.ylabel("Snødybde")
    plt.title(f"Snødybde Sirdal {input_årstall}")
   

    plt.subplot(2, 2, 2)
    plt.plot(x_datoer, nedbør_liste)
    plt.xlabel("Dato")
    plt.ylabel("Nedbør")
    plt.title(f"Nedbør Sirdal {input_årstall}")
    

    plt.subplot(2, 2, 3)
    plt.plot(x_datoer, mid_temp_liste)
    plt.xlabel("Dato")
    plt.ylabel("Middeltemperatur")
    plt.title(f"Middeltemperatur Sirdal {input_årstall}")
    

    plt.subplot(2, 2, 4)
    plt.plot(x_datoer, max_temp_liste)
    plt.xlabel("Dato")
    plt.ylabel("Maks Temperatur")
    plt.title(f"Maks Temperatur {input_årstall}")
    
    
    plt.tight_layout()
    plt.show()



