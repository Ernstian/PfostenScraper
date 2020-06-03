from bs4 import BeautifulSoup
import requests
import sys
import os
import urllib.request
import pathlib

Bretter = ["b", "int", "meta"]
GetFiles = True
DetaillierterOutput = False
Endless = True

Durchlaufnummer = 0

while True:
    Durchlaufnummer += 1
    if Endless:
        print("Durchlauf " + str(Durchlaufnummer))
    print("Zu betrachtende Bretter:")
    for Brett in Bretter:
        print(Brett)

    if GetFiles:
        print("Laden von Dateien ist aktiviert.")
    else:
        print("Laden von Dateien ist deaktiviert.")

    if DetaillierterOutput:
        print("Detaillierte Ausgabe ist aktiviert.")
    else:
        print("Detaillierte Ausgabe ist deaktiviert.")
    print("_______________________________________________________")
    for Brett in Bretter:
        print("Betrachte Brett: " + Brett)
        #Alte Pfosten auslesen
        AltePfosten = []
        AltePfostenZahl = 0
        Filename = Brett + "-Pfosten.txt"

        if os.path.exists(Filename):
            with open(Filename, "r+", encoding = "utf8") as file:
                line = file.readline()
                while line:
                    AltePfostenZahl += 1
                    AltePfosten.append(line)
                    line = file.readline()
        else:
            with open(Filename, 'w+') as file:
                AltePfostenZahl = 0


        print(str(AltePfostenZahl) + " alte Pfosten gefunden.")

        #Alle aktiven Fäden finden


        page = requests.get('https://ernstchan.xyz/' + Brett + '/catalog')

        soup = BeautifulSoup(page.text, 'html.parser')

        AlleLinks = []
        counter = 0

        for link in soup.find_all('a'):
           AlleLinks.append(link.get('href'))
           counter = counter + 1

        print(str(counter) + " URLs im Katalog gefunden.")

        FilterLinks = []
        counter = 0

        for url in AlleLinks:
           if ('/' + Brett + '/thread/' in url) & (url not in FilterLinks):
                FilterLinks.append(url)
                counter = counter + 1
        print(str(counter) + " Fäden gefunden, durchsuche...")

        #URLs zu einzelnen Fäden sind nun bekannt, suche Pfosten

        counter = 0

        Tag = []
        Monat = []
        Jahr = []
        Uhrzeit = []
        Inhalt = []
        AnzahlDateien = []
        OP = []
        Pfostennummer = []
        AllePfosten = 0
        pwd = str(pathlib.Path().absolute())

        for FadenURL in FilterLinks:
            FadenNumOfFiles = 0
            Pfostenzahl = 0
            counter = counter + 1
            Faden = requests.get("https://ernstchan.xyz" + FadenURL)
            soup = BeautifulSoup(Faden.text, 'html.parser')
            Fadennummer = FadenURL.split("/")[-1]
            if DetaillierterOutput:
                print("Kümmere mich um Faden " + str(counter) + ": /" + Brett + "/" + Fadennummer)

            for op in soup.find_all('div', {'class':'thread_OP'}): # OP hat andere Klasse als Antworten
                Pfostenzahl += 1
                for datum in op.find_all('span', {'class':'date mobile'}):
                    date = datum.text.split(" ")
                    if len(date[0][:-1]) < 2:
                        Tag.append("0" + date[0][:-1])
                    else:
                        Tag.append(date[0][:-1])
                    if date[1] == "J&aumlnner":
                        date[1] = "Januar"
                    Monat.append(date[1])
                    Jahr.append(date[2])
                    Uhrzeit.append(date[4])
                for textdiv in op.find_all('div', {'class':'text'}): # Text finden und speichern
                    for txt in textdiv.find_all('div', {'class':'post_body'}):
                        Inhalt.append(repr(txt.text))
                NumOfFiles = 0
                if not os.path.exists(pwd + "/files/" + Brett + "/" + Fadennummer + "/"):
                    os.makedirs(pwd + "/files/" + Brett + "/" + Fadennummer + "/")
                for file in op.find_all('div', {'class':'file'}):
                    NumOfFiles = NumOfFiles+1
                    if GetFiles: # Bilder finden und speichern
                        for filedata in file.find_all('a', {"target":"_blank"}):
                            fileurl = "https://ernstchan.xyz/" + filedata.attrs.get("href")
                            url = urllib.request.quote(fileurl, safe=":/")
                            extension = fileurl.split(".")[-1]
                            save = (pwd + "/files/" + Brett + "/" + Fadennummer + "/" + Fadennummer + "_" + str(NumOfFiles) + "." + extension).encode()
                            if not os.path.isfile(save):
                                try:
                                    urllib.request.urlretrieve(url, save)
                                except:
                                    pass
                AnzahlDateien.append(NumOfFiles)
                FadenNumOfFiles = FadenNumOfFiles + NumOfFiles
                Pfostennummer.append(int(Fadennummer))
                OP.append(int(Fadennummer))
                
            for pfosten in soup.find_all('div', {'class':'thread_reply'}): # Gleiches für Antworten
                    Pfostenzahl += 1
                    for datum in pfosten.find_all('span', {'class':'date mobile'}):
                        date = datum.text.split(" ")
                        if len(date[0][:-1]) < 2:
                            Tag.append("0" + date[0][:-1])
                        else:
                            Tag.append(date[0][:-1])
                        if date[1] == "J&aumlnner":
                            date[1] = "Januar"
                        Monat.append(date[1])
                        Jahr.append(date[2])
                        Uhrzeit.append(date[4])
                    for textdiv in pfosten.find_all('div', {'class':'text'}): # Pfostentext
                        for txt in textdiv.find_all('div', {'class':'post_body'}):
                            Inhalt.append(repr(txt.text))
                    NumOfFiles = 0
                    if not os.path.exists(pwd + "/files/" + Brett + "/" + Fadennummer + "/"):
                        os.makedirs(pwd + "/files/" + Fadennummer + "/")
                    for file in pfosten.find_all('div', {'class':'file'}):
                        NumOfFiles = NumOfFiles+1
                        if GetFiles: # Bilder laden
                            for filedata in file.find_all('a', {"target":"_blank"}):
                                fileurl = "https://ernstchan.xyz/" + filedata.attrs.get("href")
                                url = urllib.request.quote(fileurl, safe=":/")
                                extension = fileurl.split(".")[-1]
                                save = (pwd + "/files/" + Brett + "/" + Fadennummer + "/" + pfosten.attrs.get("id") + "_" + str(NumOfFiles) + "." + extension).encode()
                                if not os.path.isfile(save):
                                    try:
                                        urllib.request.urlretrieve(url, save)
                                    except:
                                        pass
                    AnzahlDateien.append(NumOfFiles)
                    FadenNumOfFiles = FadenNumOfFiles + NumOfFiles

                    Pfostennummer.append(int(pfosten.attrs.get("id")))
                    OP.append(int(Fadennummer))
            if DetaillierterOutput:
                print(str(Pfostenzahl) + " Pfosten mit " + str(FadenNumOfFiles) + " Dateien vorgefunden.")
            AllePfosten += Pfostenzahl

        print("Alle Fäden durchgeschaut, sortiere Pfosten...")


        PfostendataUnsorted = []
        for i in range(AllePfosten):
            newstr = Tag[i] + "-" + Monat[i] + "-" + Jahr[i] + "-" +Uhrzeit[i] + "#" + str(OP[i]) + "#" + str(Pfostennummer[i]) + "#" + str(AnzahlDateien[i]) + "#" + Inhalt[i] + "\n"
            PfostendataUnsorted.append(newstr)

        miss = 0
        for Pfosten in AltePfosten:
            if Pfosten not in PfostendataUnsorted:
                PfostendataUnsorted.append(Pfosten)
            else:
                miss += 1

        PfostendataSorted = []
        for Pfosten in PfostendataUnsorted:
            Geteilt = Pfosten.split("#", 4)
            PfostendataSorted.append((Geteilt[0], Geteilt[1], int(Geteilt[2]), Geteilt[3], Geteilt[4]))
            
        PfostendataSorted.sort(key = lambda tup: tup[2])

        Pfostendata = []
        for Pfosten in PfostendataSorted:
            Pfostendata.append(Pfosten[0] + "#" + Pfosten[1] + "#" + str(Pfosten[2]) + "#" + Pfosten[3] + "#" + Pfosten[4])
        
        print("Speichere Pfosten...")
        writtenfiles = 0
        with open(Filename, "w", encoding = "utf-8") as file:
            for Pfosten in Pfostendata:
                file.write(Pfosten)
                writtenfiles += 1
                
                           
        print("Erfolgreich " + str(writtenfiles - AltePfostenZahl) + " neue Pfosten gespeichert, " + str(miss) + " Pfosten (von " + str(AllePfosten) + " gefundenen Pfosten) waren schon gespeichert.")
        print("Es sind " + str(writtenfiles - AllePfosten) + " Pfosten gespeichert, die nicht mehr auf dem Brett sind.")
        print("Es sind jetzt " + str(writtenfiles) + " Daten in " + Filename +" gespeichert.")
        print("_______________________________________________________")
    if not Endless:
        break
input("Beehren sie uns bald wieder!")
sys.exit(0)
