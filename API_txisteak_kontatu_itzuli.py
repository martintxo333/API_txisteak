# ===================================================================================
#  TXISTEAK KONTATZEN DITUEN PROGRAMA - Martin Maiz
# Txiste bat ingelesez eta bere itzulpena euskeraz, eta beste txiste bat españolez.
#====================================================================================

"""
Bi API erabili dira: JokeAPI eta Google Translate API
Programa honek ingelesezko eta gaztelaniazko txisteak lortzen ditu JokeAPItik,
eta txisteak euskarara itzultzen ditu Google Translate API erabiliz.

Txisteen izenburuak kolore desberdinetan erakusten ditu, hizkuntzaren arabera, 
eta kontatutako txisteak gordetzen ditu testu-fitxategi batean.

Ikasitako gauza berriak eta erabilitako funtzionalitate desberdinak:
- APIak erabiltzea eta JSON erantzunak kudeatu.
- Erroreen kontrola APIek batzutan arazoak ematen zutelako (try/except-arekin).
- ANSI koloreak terminalean, hizkuntzak bereizteko.
- Datuak (txisteak) UTF-8 kodikazioarekin .txt fitxategi batean gordetzea: txisteak.txt.
- API bakoitzak erantzuteko behar duen denbora neurtzea.
- Erabiltzailearekin interaktibitatea, txiste kopurua aukeratzeko.
- Gazteleraz txistea ez errepikatzeko buklea (APIak bakarrik 6 edo 7 txiste ditu gazteleraz )
"""
#===================================================================================================
import requests
import time
from colorama import init, Fore

# Colorama hasieratu
init(autoreset=True)

# ============================================================
#  FUNTZIO OROKORRA JOKEAPI-tik TXISTEAK JASOTZEKO
# ============================================================
def lortu_txistea(url):
    """
    API-eskaera orokorra. Edozein hizkuntzatan.
    Errorea hemen kudeatzen da (try/except funtzioarekin)
    """
    try:
        hasiera = time.time()  # hasi denbora kontatzen
        erantzuna = requests.get(url, timeout=6)  # eskaera egin URL-ra
        erantzuna.raise_for_status()
        datua = erantzuna.json()  # json moduan jaso
        iraun = time.time() - hasiera  # zenbat denbora pasa dan

        # API-ak bi txiste mota ditu: esaldi batekoak (single) edo "twopart"
        if datua.get("error"):
            return "⚠️ API-k errorea itzuli du", iraun

        if datua["type"] == "single":  # txiste jarrai bat
            return datua["joke"], iraun
        else:
            return f"{datua['setup']} — {datua['delivery']}", iraun  # bi esaldiko txistea

    except Exception as e:  # errorea e aldagai bezela gorde
        return f"⚠️ Errorea APItik datuak jasotzean: {e}", 0.0


def txistea_ingelesez():
    url = "https://v2.jokeapi.dev/joke/Any?lang=en&blacklistFlags=nsfw,racist,sexist,explicit" #humore beltzeko txisteak kendu ditut (blacklistFLags=)
    return lortu_txistea(url)


def txistea_espanolez():
    url = "https://v2.jokeapi.dev/joke/Any?lang=es"
# Dohainik den API honek ere badu txisteak españolez bidaltzeko aukera (lang=es) extensioarekin, baina oso gutxi dira: 7 edo 8 txiste besterik ez
    return lortu_txistea(url)


# ============================================================
#  GOOGLE TRANSLATE API
# ============================================================
def itzuli_google(esaldia, helmuga="eu"):
    try:
        params = {
            "client": "gtx",
            "sl": "auto", # jatorrizko hizkuntza automatikoki detektatu (kasu honetan inglesa)
            "tl": helmuga, # helmugako hizkuntza (eu=euskera)
            "dt": "t",
            "q": esaldia
        }

        hasiera = time.time() # hasi kontatzen
        eskaera = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params=params,
            timeout=6
        )
        eskaera.raise_for_status()
        arr = eskaera.json()
        iraun = time.time() - hasiera # zenbat denbora pasa dan

        itzulita = "".join(seg[0] for seg in arr[0] if seg[0])
        return itzulita, iraun # jaso txistea itzulita, eta ere zenbat denbora tardatzen duen (neri etxean pila bat tardatzen zidan traduzitzen)

    except Exception as e:
        return f"⚠️ Errorea itzultzerakoan: {e}", 0.0


# ============================================================
#  TXISTEAK TEXTU FITXATEGIAN GORDE
# ============================================================
def gorde_fitxategian(en, eu, es):
    with open("txisteak.txt", "a", encoding="utf8") as f:
        # txisteak.txt: horrela deituko da artxiboa
        # a: "append" modua, txisteak gehitu artxiboan zeuden besteak borratu gabe
        # encoding="utf8": Bazpare ikur arraroak edo ñ-ak dauden españoleko txistean, bideo honetan oso ondo azalduta: https://l.eus/zer_da_UTF-8
        # with... as f: → fitxategia ireki eta f aldagaiari esleitu
        f.write("\n======= TXISTE BERRIA =======\n")
        f.write("EN: " + en + "\n")
        f.write("EUS: " + eu + "\n")
        f.write("ES: " + es + "\n")


# ============================================================
#  TXISTEA ERAKUTSI (COLORAMA)
# ============================================================
def erakutsi(en, t_en, eu, t_eu, es, t_es):
    print(Fore.CYAN + "\n🚕 Ingelesez:")
    print(en)
    print(Fore.LIGHTBLACK_EX + f"[Txistea jasotzen: {t_en:.3f}s]")

    print(Fore.GREEN + "\n🌄 Euskaraz (itzulita):")
    print(eu)
    print(Fore.LIGHTBLACK_EX + f"[Google Translate-kin itzultzen: {t_eu:.3f}s]")

    print(Fore.RED + "\n🔸 Gaztelaniaz:")
    print(es)
    print(Fore.LIGHTBLACK_EX + f"[Txistea jasotzen: {t_es:.3f}s]")


# ============================================================
#  PROGRAMA NAGUSIA
# ============================================================
def main():
    print(Fore.YELLOW + "\n================================================")
    print(Fore.YELLOW + "   API bidezko txiste-programa  – Martin Maiz")
    print(Fore.YELLOW + "================================================\n")

    print("Bi txiste kontatzen ditu: Bat ingelesez, eta euskerara itzulita; eta beste bat gazteleraz.\n")

    ikusiak_es = set() # Españolez kontatutako txisteak gordetzeko lista 
    MAX_SAIAKERAK = 10 # txiste ez errepikatuak bilatzeko dituen aukera maximoak

    while True:
        while True:
            print(Fore.BLUE + "--- MENU NAGUSIA ---")
            try:
                zenbat = int(input("Zenbat txiste nahi dituzu? "))
                if zenbat <= 0:
                    print("Mesedez, sartu zenbaki positibo bat.")
                    continue
                break
            except ValueError:
                print("Mesedez, sartu baliozko zenbaki bat.")

        for _ in range(zenbat):  # errepikatu buklea erabiltzaileak eskatutako alditan
            saiak = 0 # zenbat aldiz bilatu duen txiste EZ errepikatu bat
            while saiak < MAX_SAIAKERAK: # Bilatu maximo MAX_SAIAKERAK aurretik ikusi ez dugun txiste bat
                tx_es, t_es = txistea_espanolez()
                if tx_es not in ikusiak_es: # ziurtatu ea ez den kontatu
                    ikusiak_es.add(tx_es) # ez bada kontatu, sartu kontatutako txisteen listan
                    break
                saiak += 1 # txistea kontatuta bazegon, saiakera bat gehitu kontadorera
            else:
            # max_saiakerak ondoren ez badu txiste berririk lortzen, esan:
                print(Fore.MAGENTA + "\n⚠️ Ez dago txiste gehiagorik españolez.")
                tx_es, t_es = "—", 0.0

            # =======================
            # TXISTEA INGELESEZ
            # =======================
            tx_en, t_en = txistea_ingelesez()

            # =======================
            # EUSKERARA ITZULITAA           
            # =======================
            tx_eu, t_eu = itzuli_google(tx_en)

            # =======================
            # ERAKUTSI + GORDE
            # =======================
            erakutsi(tx_en, t_en, tx_eu, t_eu, tx_es, t_es)
            gorde_fitxategian(tx_en, tx_eu, tx_es)

            time.sleep(0.3)

        jarraitu = input("\nBeste txisterik nahi duzu? (bai/ez): ").strip().lower()
        if jarraitu != "bai":
            print("\nEskerrik asko!! :) Hurrengorarte")
            break


if __name__ == "__main__":
    main()
