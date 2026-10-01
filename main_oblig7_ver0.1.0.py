from datetime import datetime
import csv
import sys
import matplotlib.pyplot as plt

FILSTI = "Obligatoriske Innleveringer/Oblig7/sinnes_2014_2025_med_makstemperatur.csv"

#Funksjoner

def skriv_inn_årstall():
    while True:
        dato_input = input("Skriv inn et årstall (YYYY): ").strip()      #.strip() fjerner whitespace før og etter tallet
        try:
            datetime.strptime(dato_input, "%Y")      #sjekker om dato input passer i datetimeformatet "%Y" som er YYYY.
            return dato_input
        except ValueError:
            print("Årstallet må ha fire siffer.")


def tall(tekst):
    try:
        tallet = float(tekst.replace(",", "."))         #først byttes alle "," ut med "." i strengen, deretter gjøres den om til float
        return tallet                                   #hvis det er mulig returneres tallet
    except (ValueError, AttributeError):                #ValueError fanger feil hvor strengen ikke kan gjøres om til float, AttributeError for inputs som ikke kan bruke metoden .replace()
        tallet = float("nan")                           #"nan" står for Not A Number. Float funksjonen forstår dette
        return tallet


def tegn_graf(posisjon, y_verdier, enhet, navn):        #funksjon for å plotte grafer.
    plt.subplot(2,2, posisjon)                          #Parameteren posisjon brukes til subplot posisjon
    plt.plot(x_datoer, y_verdier)                       #Parameteren y_verdier brukes til å plotte y verdier
    plt.xlabel("Dato")
    plt.xticks(rotation=45)                             #Xticks (datoene) tiltes 45 grader for at de ikke skal overlappe
    plt.ylabel(f"{navn} {enhet}")                       
    plt.title(f"{navn}")

#Variabler

dato_dict = {}                  
ugyldige_datoer = []

x_datoer = []
stasjon_id_liste = []
max_temp_liste = []
mid_temp_liste = []
nedbør_liste = []
høyeste_mid_vind_liste = []
snødybde_liste = []

#Åpner fil og leser inn data fra CSV

try:
    fil = open(FILSTI, encoding="utf-8-sig", newline="")    #"utf-8-sig" fordi Byte Order Marker trolig fra lagringen av csvfilen gjør "Navn" til \ufeffNavn. sig gjør at python gjenkjenner dette og fjerner BOM.
except FileNotFoundError:
    print("Error: Filen ble ikke funnet")
    sys.exit(1)                                             #avslutter programmet med exit code 1 som indikerer at det har oppstått en feil

with fil:                                                   #med filen vi nettopp åpnet
    leser = csv.DictReader(fil, delimiter=";")              #leser filen med csv.DictReader. Delimiter=";" forteller leseren at kolonnene er separert med ";"
    
    for linje in leser:
        dato = linje.get("Tid(norsk normaltid)")            #henter verdien til kolonnen "Tid(norsk normaltid)" og putter den i variabelen dato
        try:
            datetime.strptime(dato, "%d.%m.%Y")             #sjekker om datoen passer formatet dd.mm.yyyy
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

        dato_dict[dato] = [navn, stasjon_id, max_temp, mid_temp, nedbør, høyeste_mid_vind, snødybde]            #nøkkelen dato bindes til liste med disse verdiene

#Sorterer og filtrerer basert på årstall

sortert_dict = dict(sorted(dato_dict.items(), key=lambda par: (par[0][-4:], par[0][3:5], par[0][0:2])))     #dato_dict.items() ser på key og value pair sammen.
                                                #lambda brukes som en liten funksjon for sortertingen med instrukstene under par: [0] ser på nøkkelen og [-4:] ser på de 4 siste indexene i nøkkelen dvs året.
input_årstall = skriv_inn_årstall()

for dato, verdier in sortert_dict.items():
    if dato[-4:] != input_årstall:                          #hvis året i datoen(nøkkelen) i sortert dict ikke er like input årstall hopper vi til neste iterasjon av loopen
        continue                            

    x_datoer.append(datetime.strptime(dato, "%d.%m.%Y"))    #parser datoen for denne iterasjonen og lager et nytt datetime objekt, appenderer dette til listen x_datoer
    max_temp_liste.append(tall(verdier[2]))                 #max temp har posisjon 2 (egentlig 3 hvis man teller fra 1) i listen med verdier
    mid_temp_liste.append(tall(verdier[3]))
    nedbør_liste.append(tall(verdier[4]))
    høyeste_mid_vind_liste.append(tall(verdier[5]))
    snødybde_liste.append(tall(verdier[6]))

#Melding(er) til brukeren

if not x_datoer:
    print(f"Det finnes ingen data for årstall {input_årstall}.")
    sys.exit(2)

antall_feil = len(ugyldige_datoer)
linje_tekst = "linje" if antall_feil == 1 else "linjer"
print(f"{antall_feil} {linje_tekst} ble hoppet over grunnet ugyldig format")

#Plotting

plt.figure(figsize=(12, 8))
plt.suptitle(f"Værdata Sirdal - Sinnes {input_årstall}")

tegn_graf(1, snødybde_liste, "(cm)", "Snødybde")
tegn_graf(2, nedbør_liste, "(mm)", "Nedbør")
tegn_graf(3, mid_temp_liste, "(°C)", "Middel-temperatur")
tegn_graf(4, max_temp_liste, "(°C)", "Maks-temperatur")

plt.tight_layout()
plt.show()