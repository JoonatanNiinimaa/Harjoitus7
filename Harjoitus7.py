import tkinter as tk
import random
import winsound
import time
import threading
import numpy as np  # Lisätään numpy

# Asetetaan pääikkuna ja Canvas
root = tk.Tk()
root.title("Tulivuorenpurkaus - Satunnaiset saaret")
canvas = tk.Canvas(root, width=800, height=600, bg='lightblue')  # Taustaväri merelle
canvas.pack()

# Ladataan saarten kuvat
ensimmainen_saari_img = tk.PhotoImage(file="saari.png").subsample(8, 8)  # Ensimmäisen saaren kuva
uusi_saari_img = tk.PhotoImage(file="uusisaari.png").subsample(4, 4)    # Kaikkien muiden saarien kuva

# Ladataan apinan kuva
apina_img = tk.PhotoImage(file="monkey.png").subsample(20, 20)  # Pienennetään apinan kuva

# Ladataan hain kuva
shark_img = tk.PhotoImage(file="shark.png").subsample(10, 10)  # Pienennetään hain kuva

# Saarten tietojen tallentaminen (koko ja sijainti)
saaret = []
saari_laskuri = 1  # Ensimmäisen saaren nimi on s1, seuraavan s2 jne.
apinat_lkm_label = None  # Apinoiden lukumäärän label
matka_label = None  # Matkalaskurin label

# Määritetään saaren koko siten, että merelle mahtuu noin 10 saarta
saari_koko = 80  # Tämä on saaren kuvakkeen oletuskoko
min_etaisyys = 100  # Määritetään minimietäisyys saarien välille

# Funktio, joka tarkistaa, osuuko uusi saari liian lähelle aiempia saaria
def onko_paatteinen(x, y):
    # Tarkistetaan etäisyys ensimmäiseen saareen
    if saaret:
        saari_x, saari_y = saaret[0]['x'], saaret[0]['y']
        etaisyys = ((x - saari_x) ** 2 + (y - saari_y) ** 2) ** 0.5
        if etaisyys < min_etaisyys:
            return True
    
    # Tarkistetaan etäisyys kaikkiin muihin saariin
    for saari in saaret[1:]:
        saari_x, saari_y = saari['x'], saari['y']
        etaisyys = ((x - saari_x) ** 2 + (y - saari_y) ** 2) ** 0.5
        if etaisyys < min_etaisyys:
            return True
    return False

# Funktio, joka tarkistaa apinan kuoleman riskin
def tarkista_kuolema():
    return random.random() < 0.01  # 1% riski

# Funktio, joka tarkistaa saarella olevat apinat ja poistaa kuolleet
def tarkista_apinat_kuolema(saari):
    apinat = saari['apinat']
    kuolleet = 0  # Lasketaan kuolleiden määrä
    for apina in apinat[:]:  # Käytetään viipaletta, jotta voimme muokata listaa
        if tarkista_kuolema():  # Tarkistetaan kuoleman riski
            winsound.PlaySound("nauru.wav", winsound.SND_FILENAME)
            canvas.delete(apina['obj'])  # Poistetaan apina kanvaalta
            apinat.remove(apina)  # Poistetaan apina listasta
            kuolleet += 1  # Lisätään kuollut

    # Päivitetään apinoiden määrä käyttöliittymässä
    paivita_apinat_lkm()  # Tämä kutsu ei vaadi argumenttia

# Funktio, joka tarkistaa kaikkien saarten apinat kymmenen sekunnin välein
def tarkista_kuolemat():
    while True:
        for saari in saaret:
            tarkista_apinat_kuolema(saari)
        time.sleep(10)  # Odotetaan 10 sekuntia

# Funktio, joka tuottaa apinan äänen
def apinan_aantely(taajuus):
    if taajuus:  # Tarkistetaan, onko taajuus määritelty
        winsound.Beep(taajuus, 500)  # Soitetaan apinan ääni 0,5 sekunnin ajan


# Funktio, joka tuottaa apinoiden äänet
def tuota_apina_aanet(apinat):
    while True:
        if aanet_soimassa:  # Tarkistetaan lippu
            for apina in apinat:
                taajuus = apina['taajuus']
                apinan_aantely(taajuus)
                time.sleep(random.randint(8, 12))  # Odota 8-12 sekuntia
        else:
            time.sleep(1)  # Odotetaan hetki ennen tarkistamista uudelleen
            print("EI taajuuksia")


# Funktio, joka lisää 10 apinaa saarelle
def lisaa_apinat_saarelle(x, y, matkustaa=False):
    global apinat
    apinat = []  # Tyhjennetään apinoiden lista
    taajuus = random.randint(400, 2000)  # Luodaan satunnainen taajuus

    for i in range(20):  # Lisää 10 apinaa
        apina_x = random.randint(x - saari_koko // 3, x + saari_koko // 3)
        apina_y = random.randint(y - saari_koko // 3, y + saari_koko // 3)
        
        apina_obj = canvas.create_image(apina_x, apina_y, image=apina_img)
        
        # Luodaan apinan sanakirja, jossa on osaa_matkustaa
        apinat.append({'x': apina_x, 'y': apina_y, 'taajuus': taajuus, 'obj': apina_obj, 'osaa_matkustaa': matkustaa})

    if apinat:  # Varmistetaan, että apinoita on, ennen kuin aloitetaan äänet
        threading.Thread(target=tuota_apina_aanet, args=(apinat,), daemon=True).start()

    return apinat  # Palautetaan apinoiden lista


# Funktio, joka luo uuden satunnaisen saaren (käyttäen uusisaari.png)
def luo_satunnainen_saari():
    global saari_laskuri  # Tuodaan saari_laskuri globaaliksi

    # Tarkistetaan, onko saaria olemassa
    if len(saaret) == 0:  # Jos ei ole saaria
        luo_ensimmainen_saari()  # Kutsutaan ensimmainen saari -funktiota
        return  # Lopetetaan funktio, ei jatketa saaren luontia

    # Jos saaria on, luodaan uusi satunnainen saari
    while True:
        x = random.randint(saari_koko, 800 - saari_koko)
        y = random.randint(saari_koko, 600 - saari_koko)

        if not onko_paatteinen(x, y):
            break

    saari_obj = canvas.create_image(x, y, image=uusi_saari_img)
    saari_nimi = f"s{saari_laskuri}"
    saari_laskuri += 1

    # Sijoita saaren nimi keskelle
    nimi_obj = canvas.create_text(x, y, text=saari_nimi, fill="black", font=("Arial", 12))
    
    # Apinoiden lisääminen saarelle
    apinat = lisaa_apinat_saarelle(x, y, matkustaa=False)  # Matkustaa=False
    apinat_lkm = len(apinat)  # Apinoiden määrä

    # Sijoita apinoiden määrä keskelle saarta
    apinat_lkm_label = canvas.create_text(x, y + 20, text=f"Apinoita: {apinat_lkm}", fill="black", font=("Arial", 10))

    # Tallennetaan apinat, nimi ja apinoiden määrä
    saaret.append({'x': x, 'y': y, 'obj': saari_obj, 'nimi': saari_nimi, 'nimi_obj': nimi_obj, 'apinat': apinat, 'apinat_lkm_label': apinat_lkm_label})

    winsound.PlaySound("purkaus.wav", winsound.SND_FILENAME)
    global aanet_soimassa
    aanet_soimassa = True
    paivita_apinat_lkm()  # Päivitetään apinoiden määrä saaren lisäämisen yhteydessä


# Luo ensimmäinen saari keskelle merta (käyttäen saari.png)
def luo_ensimmainen_saari():
    global saari_laskuri, aanet_soimassa
    aanet_soimassa = True

    x = 400
    y = 300
    saari_obj = canvas.create_image(x, y, image=uusi_saari_img)

    saari_nimi = "s1"
    saari_laskuri += 1

    # Sijoita saaren nimi keskelle
    nimi_obj = canvas.create_text(x, y, text=saari_nimi, fill="black", font=("Arial", 12))
    
    # Apinoiden määrä
    apinat_lkm_label = canvas.create_text(x, y + 20, text="Apinoita: 10", fill="black", font=("Arial", 10))  # Apinoiden määrä

    apinat = lisaa_apinat_saarelle(x, y, matkustaa=True)  # Matkustaa=True ensimmäiselle saarelle

    lisaa_laiturit(x, y, saari_nimi)

    # Tallennetaan apinat, nimi ja apinoiden määrä
    saaret.append({'x': x, 'y': y, 'obj': saari_obj, 'nimi': saari_nimi, 'nimi_obj': nimi_obj, 'apinat': apinat, 'apinat_lkm_label': apinat_lkm_label})
    paivita_apinat_lkm()  # Päivitetään apinoiden määrä saaren lisäämisen yhteydessä

def lisaa_laiturit(saaren_x, saaren_y, saari_nimi):
    laiturin_pituus = 5
    laiturin_leveys = 15
    laiturin_VO_etäisyys = 5  # Etäisyys saaresta (vasen ja oikea)
    laiturin_YA_etäisyys = 15  # Etäisyys saaresta (ylä ja ala)

    # Saari on suorakaiteen muotoinen
    saaren_leveys = saari_koko  # Saari on leveä (x-akseli)
    saaren_korkeus = saari_koko // 2  # Saari on korkea (y-akseli)

    # Ylälaituri
    canvas.create_rectangle(saaren_x - laiturin_pituus // 2, 
                            saaren_y - saaren_korkeus // 2 - laiturin_leveys - laiturin_YA_etäisyys,
                            saaren_x + laiturin_pituus // 2, 
                            saaren_y - saaren_korkeus // 2 - laiturin_YA_etäisyys,
                            fill="brown")  # Ylälaiturin väri

    # Alalaituri
    canvas.create_rectangle(saaren_x - laiturin_pituus // 2, 
                            saaren_y + saaren_korkeus // 2 + laiturin_YA_etäisyys,
                            saaren_x + laiturin_pituus // 2, 
                            saaren_y + saaren_korkeus // 2 + laiturin_leveys + laiturin_YA_etäisyys,
                            fill="brown")  # Alalaiturin väri

    # Vasemmat laiturit
    canvas.create_rectangle(saaren_x - saaren_leveys // 2 - laiturin_leveys - laiturin_VO_etäisyys, 
                            saaren_y - laiturin_pituus // 2,
                            saaren_x - saaren_leveys // 2 - laiturin_VO_etäisyys, 
                            saaren_y + laiturin_pituus // 2,
                            fill="brown")  # Vasemman laiturin väri
    

    # Oikeat laiturit
    canvas.create_rectangle(saaren_x + saaren_leveys // 2 + laiturin_VO_etäisyys, 
                            saaren_y - laiturin_pituus // 2,
                            saaren_x + saaren_leveys // 2 + laiturin_leveys + laiturin_VO_etäisyys, 
                            saaren_y + laiturin_pituus // 2,
                            fill="brown")  # Oikean laiturin väri


# Lipun määrittely, joka estää vanhojen äänten soimisen
aanet_soimassa = False

# Funktio, joka tyhjentää kaikki saaret
def tyhjennä_saaret():
    global saaret, aanet_soimassa, saari_laskuri, apinat
    
    aanet_soimassa = False
    apinat.clear()  # Tyhjennetään apinalista (poistetaan taajuudet ja muut tiedot)
    saaret.clear()  # Tyhjennetään saarten lista
    saari_laskuri = 1
    canvas.delete("all")  # Tyhjennetään kanva


# Funktio, joka päivittää apinoiden määrän käyttöliittymässä
def paivita_apinat_lkm():
    elossa_apinat = sum(len(saari['apinat']) for saari in saaret)  # Lasketaan kaikkien saarten apinat
    if apinat_lkm_label:
        apinat_lkm_label.config(text=f"Apinoita elossa: {elossa_apinat}")

    # Päivitetään myös jokaisen saaren apinoiden määrä
    for saari in saaret:
        canvas.itemconfig(saari['apinat_lkm_label'], text=f"Apinoita: {len(saari['apinat'])}")

def lahetta_apina_uimaan():
    """Lähettää satunnaisen apinan uimaan satunnaisiin suuntiin."""
    for saari in saaret:
        if saari['apinat']:  # Tarkistetaan, onko saarella apinoita
            # Suodatetaan vain apinat, jotka osaavat uida
            uivat_apinat = [apina for apina in saari['apinat'] if apina['osaa_matkustaa']]
            
            if uivat_apinat:  # Jos on apinoita, jotka osaavat uida
                apina = random.choice(uivat_apinat)  # Valitaan satunnainen apina
                saari['apinat'].remove(apina)  # Poistetaan apina saaresta

                # Lasketaan laiturien sijainnit
                x = saari['x']
                y = saari['y']
                laiturit = [
                    (x, y - saari_koko // 2),  # Pohjoinen
                    (x + saari_koko // 2, y),  # Itäinen
                    (x, y + saari_koko // 2),  # Eteläinen
                    (x - saari_koko // 2, y)   # Lännen
                ]
                
                # Valitaan satunnainen laiturin sijainti
                laiturin_sijainti = random.choice(laiturit)

                # Liikuta apinaa laiturille ensin
                canvas.move(apina['obj'], laiturin_sijainti[0] - apina['x'], laiturin_sijainti[1] - apina['y'])
                apina['x'], apina['y'] = laiturin_sijainti  # Aseta apina laiturille
                
                # Aloita uinnin satunnaiset suuntia
                def ui_satunnaisesti():
                    while True:  # Tämä silmukka toimii niin kauan kuin apina ui
                        # Valitaan satunnainen suunta jokaisen siirron yhteydessä
                        suunta = random.choice(['pohjoinen', 'ita', 'etelä', 'länsi'])
                        print(f"Apina liikkuu suuntaan: {suunta}")  # Tulostetaan valittu suunta

                        # Tarkista canvasin rajat ja liikuta apinaa
                        if suunta == 'pohjoinen':
                            if apina['y'] > 0:
                                apina['y'] -= 40
                        elif suunta == 'ita':
                            if apina['x'] < canvas.winfo_width():
                                apina['x'] += 40
                        elif suunta == 'etelä':
                            if apina['y'] < canvas.winfo_height():
                                apina['y'] += 40
                        elif suunta == 'länsi':
                            if apina['x'] > 0:
                                apina['x'] -= 40

                        # Siirretään apinaa kanvassa
                        canvas.coords(apina['obj'], apina['x'], apina['y'])
                        winsound.PlaySound("swim_sound.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)  
                        canvas.update()  # Päivitä canvas

                        # Tarkista, kuoleeko apina hain hyökkäyksessä
                        if tarkista_kuolema():
                            current_x = apina['x']  # Apinan nykyinen x-koordinaatti
                            current_y = apina['y']  # Apinan nykyinen y-koordinaatti
                            canvas.coords(apina['obj'], -100, -100)  # Poista apina näkyvistä
                            canvas.create_image(current_x, current_y, image=shark_img)  # Lisää hai kuva apinan kuoleman sijaintiin
                            winsound.PlaySound("shark_sound.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)  # Soita hai-ääni
                            saari['apinat'].remove(apina)  # Poista apina saaresta
                            paivita_apinat_lkm()  # Päivitä apinoiden määrä
                            return  # Lopeta apinan uiminen, koska apina kuoli

                        # Tarkista, onko apina päässyt millekään muulle saarelle
                        for kohdesaari in saaret:
                            if kohdesaari != saari:  # Varmistetaan, ettei tarkisteta samaa saarta
                                if (kohdesaari['x'] - saari_koko // 2 <= apina['x'] <= kohdesaari['x'] + saari_koko // 2 and
                                    kohdesaari['y'] - saari_koko // 2 <= apina['y'] <= kohdesaari['y'] + saari_koko // 2):
                                    
                                    # Apina on päässyt toisen saaren alueelle
                                    print(f"Apina {apina['obj']} on päässyt saarelle {kohdesaari['nimi']}!")

                                    # Poistetaan apina kanvasta
                                    canvas.delete(apina['obj'])  
                                    # Lisää uusi apina kohdesaaren apinat-listaan
                                    uusi_apina = {
                                        'x': random.randint(kohdesaari['x'] - saari_koko // 3, kohdesaari['x'] + saari_koko // 3),
                                        'y': random.randint(kohdesaari['y'] - saari_koko // 3, kohdesaari['y'] + saari_koko // 3),
                                        'obj': canvas.create_image(kohdesaari['x'], kohdesaari['y'], image=apina_img),
                                        'taajuus': 0,
                                        'osaa_matkustaa': True  # Aseta osaa_matkustaa True
                                    }
                                    kohdesaari['apinat'].append(uusi_apina)
                                    print(f"Uusi apina on lisätty saarelle {kohdesaari['nimi']}!")
                                    return  # Poistutaan silmukasta

                        time.sleep(10)  # Odota 10 sekuntia ennen seuraavaa liikettä

                # Käynnistä säie apinan uimiseen
                threading.Thread(target=ui_satunnaisesti, daemon=True).start()
                break  # Lopeta silmukka, kun apina on lähetetty uimaan

def laheta_10_apinaa_uimaan():
    for i in range(10):  # Lähetetään 10 apinaa
        lahetta_apina_uimaan()  # Lähetetään yksi apina uimaan
        time.sleep(10)  # Odotetaan 10 sekuntia ennen kuin lähetetään seuraava apina

# Tarkistetaan osaavatko apinat uida ja tätä osaamista tarkastellaan 5s välein.
# Jos apinat osaavat uida niin he tekevät laiturin
def tarkista_uimataito():
    for saari in saaret:
        saari_nimi = saari['nimi']
        uimaan_osaa = any(apina['osaa_matkustaa'] for apina in saari['apinat'])
        
        if uimaan_osaa:
            lisaa_laiturit(saari['x'], saari['y'], saari_nimi)

def tarkista_uimataito_thread():
    while True:
        tarkista_uimataito()
        time.sleep(5)

threading.Thread(target=tarkista_uimataito_thread, daemon=True).start()


# Luo käyttöliittymään nappi tulivuorenpurkaus
tulivuorenpurkaus_nappi = tk.Button(root, text="Tulivuorenpurkaus", command=luo_satunnainen_saari)
tulivuorenpurkaus_nappi.pack()

# Luo käyttöliittymään nappi saarten tyhjentämiselle
tyhjenna_nappi = tk.Button(root, text="Tyhjennä saaret", command=tyhjennä_saaret)
tyhjenna_nappi.pack()

# Luo käyttöliittymään nappi apinan lähettämiseksi uimaan
lahetta_apina_nappi = tk.Button(root, text="Lähetä apina uimaan", command=lahetta_apina_uimaan)
lahetta_apina_nappi.pack()

# Luodaan nappi, joka aloittaa apinoiden lähettämisen
laheta_button = tk.Button(root, text="Lähetä 10 apinaa uimaan", command=lambda: threading.Thread(target=laheta_10_apinaa_uimaan, daemon=True).start())
laheta_button.pack()

# Luo label apinoiden eloonjäämislaskurille
apinat_lkm_label = tk.Label(root, text="Apinoita elossa: 0")
apinat_lkm_label.pack()

# Käynnistetään säie kuoleman tarkistamiselle
threading.Thread(target=tarkista_kuolemat, daemon=True).start()

# Luodaan ensimmäinen saari
luo_ensimmainen_saari()

# Ajetaan pääsilmukka
root.mainloop()
