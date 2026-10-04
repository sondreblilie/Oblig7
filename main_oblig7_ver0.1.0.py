from datetime import datetime
import csv
import sys
import matplotlib.pyplot as plt

FILSTI = "Obligatoriske Innleveringer/Oblig7/sinnes_2014_2025_med_makstemperatur.csv"

#Funksjoner

def skriv_inn_årstall():
    while True:
        dato_input = input("\nSkriv inn et årstall (YYYY): ").strip()      #.strip() fjerner whitespace før og etter tallet
        try:
            datetime.strptime(dato_input, "%Y")                            #sjekker om dato input passer i datetimeformatet "%Y" som er YYYY.
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


def tegn_graf(posisjon, x_verdier, dato, y_verdier, enhet, navn):        #funksjon for å plotte grafer.
    plt.subplot(2,2, posisjon)                          #Parameteren posisjon brukes til subplot posisjon
    plt.plot(x_verdier, y_verdier)                       #Parameteren y_verdier brukes til å plotte y verdier
    plt.xlabel(dato)
    plt.xticks(rotation=45)                             #Xticks (datoene) tiltes 45 grader for at de ikke skal overlappe
    plt.ylabel(f"{navn} {enhet}")                       
    plt.title(f"{navn}")

#Åpner fil og leser inn data fra CSV

dato_dict = {}                  
ugyldige_datoer = []

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

        dato_dict[dato] = [navn, stasjon_id, max_temp, mid_temp, nedbør, høyeste_mid_vind, snødybde]        #nøkkelen dato bindes til liste med disse verdiene

#Sorterer og filtrerer basert på årstall

x_datoer = []
stasjon_id_liste = []
max_temp_liste = []
mid_temp_liste = []
nedbør_liste = []
høyeste_mid_vind_liste = []
snødybde_liste = []

sortert_dict = dict(sorted(dato_dict.items(), key=lambda par: (par[0][-4:], par[0][3:5], par[0][0:2])))     #dato_dict.items() ser på key og value pair sammen.
                                                            #lambda brukes som en liten funksjon for sortertingen med instrukstene under par: [0] ser på nøkkelen og [-4:] ser på de 4 siste indexene i nøkkelen dvs året.
input_årstall = skriv_inn_årstall()
år = int(input_årstall)

for dato, verdier in sortert_dict.items():
    if dato[-4:] != input_årstall:                          #hvis året i datoen(nøkkelen) i sortert dict ikke er like input årstall hopper vi til neste iterasjon av loopen
        continue                            

    x_datoer.append(datetime.strptime(dato, "%d.%m.%Y"))    #parser datoen for denne iterasjonen og lager et nytt datetime objekt, appenderer dette til listen x_datoer
    max_temp_liste.append(tall(verdier[2]))                 #max temp har posisjon 2 (egentlig 3 hvis man teller fra 1) i listen med verdier
    mid_temp_liste.append(tall(verdier[3]))
    nedbør_liste.append(tall(verdier[4]))
    høyeste_mid_vind_liste.append(tall(verdier[5]))
    snødybde_liste.append(tall(verdier[6]))

if not x_datoer:
    print(f"\n- Det finnes ingen data for årstall {input_årstall}.\n")
    sys.exit(2)
else:
    print(f"{"VÆRDATA SIRDAL - SINNES":=^90}")

#Finner snødager i skisesongen mellom november forrige år og mai det året.

start_dato = datetime.strptime(f"01.11.{år-1}", "%d.%m.%Y")
slutt_dato = datetime.strptime(f"01.05.{år}", "%d.%m.%Y")
antall_snødager = 0

for dato, verdier in sortert_dict.items():
    dato_obj = datetime.strptime(dato, "%d.%m.%Y")
    if dato_obj < slutt_dato and dato_obj >= start_dato and tall(verdier[6]) >= 20:
        antall_snødager += 1

print(f"\n- Det var {antall_snødager} dager med minst 20 cm snødybde i skisesongen {år-1}/{år}.")

#Plantevekst

start_dato_plante = datetime.strptime(f"01.01.{år}", "%d.%m.%Y")
slutt_dato_plante = datetime.strptime(f"31.12.{år}", "%d.%m.%Y")
plantevekst = 0

for dato, verdier in sortert_dict.items():
    dato_obj = datetime.strptime(dato, "%d.%m.%Y")
    
    if dato_obj >= start_dato_plante and dato_obj <= slutt_dato_plante and tall(verdier[3]) >= 5:
        plantevekst += tall(verdier[3]) - 5

print(f"\n- Total plantevekst var {round(plantevekst)} for året {år}.")

#Lengste periode uten nedbør

nedbør_dict = {}
lengste_dict = {}

for dato, verdier in sortert_dict.items():              #for hvert key value pair i sortert_dict.items(). Items() gjør at vi får paret. .values() hadde gitt oss verdiene kun. .keys() hadde gitt oss nøklene kun.
    if tall(verdier[4]) == 0:                           #funksjonen tall (lagd tidligere) brukes her for å gjøre verdier[4] (nedbør) om til tall, samt bytte ut "," med "." og gjøre manglende verdier om til "nan"
        nedbør_dict[dato] = verdier[4]                  #key value pair (dato: nedbør) legges til nedbør_dict hvis nedbør er 0
    else:
        if len(nedbør_dict) > len(lengste_dict):        #lengste_dict settes til nedbør_dict hvis nedbør_dict er lengre
            lengste_dict = nedbør_dict.copy()
        nedbør_dict.clear()                             #nedbør_dict tømmes

if len(nedbør_dict) > len(lengste_dict):                #sjekken gjøres igjen, i tilfelle for loopen slutter på en tørr dag (og vi aldri får gjort else checken)
    lengste_dict = nedbør_dict.copy()

lengste_dict_nøkler = list(lengste_dict.keys())         #lager en liste av nøklene (datoene) i lengste_dict

print(f"\n- Lengste periode uten nedbør var på {len(lengste_dict)} dager, fra {lengste_dict_nøkler[0]} til {lengste_dict_nøkler[-1]}."
      f"\n  Dette er basert på all dataen, ikke dataen for året {input_årstall}.")

#Antall sommerdager, høysommerdager og tropedager

antall_sommerdager = 0
antall_høysommerdager = 0
antall_tropedager = 0

start_dato_sommerdager = datetime.strptime(f"01.01.{år}", "%d.%m.%Y")
slutt_dato_sommerdager = datetime.strptime(f"31.12.{år}", "%d.%m.%Y")

for dato, verdier in sortert_dict.items():
    dato_obj = datetime.strptime(dato, "%d.%m.%Y")
    if dato_obj >= start_dato_sommerdager and dato_obj <= slutt_dato_sommerdager:
        if 20 <= tall(verdier[2]) < 25:     #Hvis oppgaven mener en dag kan være en tropedag, høysommerdag og sommerdag samtidig
            antall_sommerdager +=1          #gjør vi elif om til if og fjerner øvre grense av sammenlikningen.
        elif 25 <= tall(verdier[2]) < 30:
            antall_høysommerdager += 1
        elif 30 <= tall(verdier[2]):
            antall_tropedager += 1

print(f"\n- Det var {antall_sommerdager} sommerdager, {antall_høysommerdager} høysommerdager og {antall_tropedager} tropedager i {input_årstall}.")


#Melding(er) til brukeren

antall_feil = len(ugyldige_datoer)
if antall_feil != 0:
    linje_tekst = "linje" if antall_feil == 1 else "linjer"
    print(f"\n- {antall_feil} {linje_tekst} ble hoppet over grunnet ugyldig format\n")

#Plotting

plt.figure(figsize=(12, 8))
plt.suptitle(f"Værdata Sirdal - Sinnes {input_årstall}")

tegn_graf(1, x_datoer, "Dato", snødybde_liste, "(cm)", "Snødybde")
tegn_graf(2, x_datoer, "Dato", nedbør_liste, "(mm)", "Nedbør")
tegn_graf(3, x_datoer, "Dato", mid_temp_liste, "(°C)", "Middeltemperatur")
tegn_graf(4, x_datoer, "Dato", max_temp_liste, "(°C)", "Makstemperatur")

plt.tight_layout()
plt.show()