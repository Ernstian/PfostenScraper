import sqlite3
import matplotlib.pyplot as plt
import datetime
from calendar import monthrange
import os

Database = "Pfosten.db"


Bretter = ["b", "int", "meta"]
Savefolder = os.getcwd() + "/Results/"


for Brett in Bretter:
    connection = sqlite3.connect(Database)
    cursor = connection.cursor()
    executestring = "SELECT Tag, Monat, Jahr FROM Pfosten WHERE Brett = '" + str(Brett) + "'"
    cursor.execute(executestring)
    Results = cursor.fetchall()
    Werte = {}
    # Start: 1. Juni 2018
    # End: Today
    Monate = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    now = datetime.datetime.now()
    curyear = now.year
    curmon = Monate[now.month-1]
    curday = now.day
    curhour = now.hour
    curmin = now.minute
    cursec = now.second
    Jahre = []
    Werte = {}
    for i in range(curyear - 2018 + 1):
        Jahre.append(2018 + i)
    
    for year in Jahre:
        if year == 2018:
            for month in Monate[5:]:
                (Monatsanfang, Monatsende) = monthrange(year, Monate.index(month)+1)
                for i in range(Monatsende):
                    Werte[(i+1, month, year)] = 0
        else:
            if year == curyear:
                for month in Monate[:Monate.index(curmon)+1]:
                    if month == curmon:
                        for i in range(curday):
                            Werte[(i+1, month, year)] = 0
                    else:
                        (Monatsanfang, Monatsende) = monthrange(year, Monate.index(month)+1)
                        for i in range(Monatsende):
                            Werte[(i+1, month, year)] = 0
            else:
                for month in Monate:
                    (Monatsanfang, Monatsende) = monthrange(year, Monate.index(month)+1)
                    for i in range(Monatsende):
                        Werte[(i+1, month, year)] = 0                    
    xachse = []
    i = 6
    for (T, M, J) in list(Werte.keys()):
        i += 1
        if i % 7 == 0:
            xachse.append((T, M, J))
            i = 0
    
    
    for (Tag, Monat, Jahr) in Results:
        Werte[(Tag, Monat, Jahr)] += 1
    fig = plt.gcf()
    fig.set_size_inches((60, 30), forward=False)
    plt.locator_params(axis='x', nbins=7)
    plt.bar(range(len(Werte)), Werte.values())
    plt.xticks(range(0, len(Werte), 7), xachse, rotation = 90)
    plt.title(Brett)
    plt.xlabel("Datum")
    plt.ylabel("Pfosten/Tag")
    plt.grid(True)

    Save = Savefolder + str(Brett) + "-Auswertung-" + str(curday) + "-" + str(curmon) + "-" + str(curyear) + "-" + str(curhour) + "-" + str(curmin) + "-" + str(cursec) +".jpg"

    fig.savefig(Save, dpi=500)
    fig.clear()
