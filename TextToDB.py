import sqlite3
import os
import sys

Database = "Pfosten.db"
Bretter = ["b", "int", "meta"]

if not os.path.isfile(Database):
    connection = sqlite3.connect(Database)
    cursor = connection.cursor()
    sql_command = """
        CREATE TABLE Pfosten (
        Brett VARCHAR(10),
        Fadennummer INTEGER,
        Pfostennummer INTEGER,
        Tag INTEGER,
        Monat VARCHAR(20),
        Jahr INTEGER,
        Uhrzeit VARCHAR(20),
        Dateienzahl INTEGER,
        Text VARCHAR(99999),  
        PRIMARY KEY (Brett, Pfostennummer));"""
    cursor.execute(sql_command)
    connection.commit()
    connection.close()
    
connection = sqlite3.connect(Database)
cursor = connection.cursor()

for Brett in Bretter:
    AltePfosten = []
    Filename = Brett + "-Pfosten.txt"
    if os.path.exists(Filename):
        with open(Filename, "r+", encoding = "utf8") as file:
            line = file.readline()
            while line:
                AltePfosten.append(line)
                line = file.readline()
    else:
        print("Fehler: " + Filename + " nicht gefunden")
        sys.exit(1)

    SplitPfosten = []    
    for Pfosten in AltePfosten:
        Hilfsstring = Pfosten.split("#", 4)
        DateSplit = Hilfsstring[0].split("-", 3)
        Tag = DateSplit[0]
        Monat = DateSplit[1]
        Jahr = DateSplit[2]
        Uhrzeit = DateSplit[3]
        Fadennummer = Hilfsstring[1]
        Pfostennummer = Hilfsstring[2]
        Dateienzahl = Hilfsstring[3]
        Text = Hilfsstring[4]
        cursor.execute("INSERT or IGNORE INTO Pfosten VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (Brett, Fadennummer, Pfostennummer, Tag, Monat, Jahr, Uhrzeit, Dateienzahl, Text))
    connection.commit()
connection.close()
print("Erfolgreich in die Datenbank geschrieben.")
            
