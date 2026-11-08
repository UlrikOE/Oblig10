import csv
import glob
from datetime import datetime
from matplotlib import pyplot as plt
from statistics import median

dato = []
maks_måned = []
min_måned = []
maks_snødybde = []
tot_nedbør = []
maks_midvind = []



månedsdata = {}
maks_per_måned = {}
min_per_måned = {}
maks_snødybde_måned = {}
tot_nedbør_måned = {}
maks_midvind_måned = {}
stasjoner = {}

filer = glob.glob("Værdata/*.csv")


for fil in filer:
    with open(fil, "r", encoding="utf-8") as fila:
        leser = csv.reader(fila, delimiter=";")
        next(leser)

        for rad in leser:
            stasjonsnavn = rad[0]
            stasjonsnummer = rad[1].strip()

            if stasjonsnummer.startswith("SN"):
                stasjoner[stasjonsnummer] = stasjonsnavn


for stasjonsnummer in stasjoner:
    print(stasjonsnummer, stasjoner[stasjonsnummer])

while True:
    stasjon_valg = input("Skriv inn stasjonsnummer: ").strip()

    if stasjon_valg not in stasjoner:
        print("Ugyldig stasjonsnummer!")
    else:
        break

for fil in filer:
    with open(fil, "r", encoding="utf-8") as fila:
        leser = csv.reader(fila, delimiter=";")
        next(leser)

        for rad in leser:
            if rad[1].strip() != stasjon_valg:
                continue

            if rad[2].strip() == "":
                continue

            dato = datetime.strptime(rad[2], "%d.%m.%Y")

            år_måned = (dato.year, dato.month)

            if år_måned in månedsdata:
                månedsdata[år_måned].append(rad)
            else:
                månedsdata[år_måned] = [rad]

for år_måned in månedsdata:
    mid_temp = []
    snødybde = []
    nedbør = []
    høy_midvind = []

    for rad in månedsdata[år_måned]:


        if rad[4].strip() != "-" and rad[4].strip() != "":
            mid_temp.append(float(rad[4].strip().replace(",", ".")))

        if rad[7].strip() != "-" and rad[7].strip() != "":
            snødybde.append(float(rad[7].strip().replace(",", ".")))

        if rad[5].strip() != "-" and rad[5].strip() != "":
            nedbør.append(float(rad[5].strip().replace(",", ".")))

        if rad[6].strip() != "-" and rad[6].strip() != "":
            høy_midvind.append(float(rad[6].strip().replace(",", ".")))

            if høy_midvind:
                maks_midvind = max(høy_midvind)
                maks_midvind_måned[år_måned] = maks_midvind
                 #   print(år_måned, maks_midvind)


            if len(nedbør) > 20:
                tot_nedbør = sum(nedbør)
                tot_nedbør_måned[år_måned] = tot_nedbør
                #    print(år_måned,tot_nedbør)
                #else:
                 #  print("Ikke nok nedbørsdager! ")


            if snødybde:
                maks_snødybde = max(snødybde)
                maks_snødybde_måned[år_måned] = maks_snødybde
                    #print(år_måned, maks_snødybde)

            if mid_temp:
                maks_måned = max(mid_temp)
                maks_per_måned[år_måned] = maks_måned
                min_måned = min(mid_temp)
                min_per_måned[år_måned] = min_måned
                    #print(år_måned, maks_måned)
                    #print(år_måned, min_måned)



datoer = []
snødybder = []

for år_måned in sorted(maks_snødybde_måned):
    snødybder.append(maks_snødybde_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1], 1)
    datoer.append(dato)

nedbør_datoer = []
nedbør_verdier = []

for år_måned in sorted(tot_nedbør_måned):
    nedbør_verdier.append(tot_nedbør_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1], 1)
    nedbør_datoer.append(dato)

maks_temp_verdier = []
maks_temp_datoer = []

for år_måned in sorted(maks_per_måned):
    maks_temp_verdier.append(maks_per_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1], 1)
    maks_temp_datoer.append(dato)

min_temp_verdier = []
min_temp_datoer = []

for år_måned in sorted(min_per_måned):
    min_temp_verdier.append(min_per_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1],1)
    min_temp_datoer.append(dato)

maks_midvind_verdier = []
maks_midvind_datoer = []

for år_måned in sorted(maks_midvind_måned):
    maks_midvind_verdier.append(maks_midvind_måned[år_måned])
    dato = datetime(år_måned[0], år_måned[1],1)
    maks_midvind_datoer.append(dato)

fig, ax = plt.subplots(5, 1, figsize=(12,10), sharex=True)

ax[0].plot(datoer, snødybder)
ax[1].plot(nedbør_datoer, nedbør_verdier)
ax[2].plot(maks_temp_datoer, maks_temp_verdier)
ax[3].plot(min_temp_datoer, min_temp_verdier)
ax[4].plot(maks_midvind_datoer, maks_midvind_verdier)

ax[0].set_ylabel("cm")
ax[1].set_ylabel("mm")
ax[2].set_ylabel("°C")
ax[3].set_ylabel("°C")
ax[4].set_ylabel("m/s")

ax[0].set_title("Maks Snødybde")
ax[1].set_title("Total Nedbør")
ax[2].set_title("Maks Temperatur")
ax[3].set_title("Min Temperatur")
ax[4].set_title("Maks Middelvind")

plt.tight_layout()


sommerdager = {}
høysommerdager = {}
tropedager = {}

for år_måned in månedsdata:

    år = år_måned[0]

    if år not in sommerdager:
        sommerdager[år] = 0
        høysommerdager[år] = 0
        tropedager[år] = 0

    for rad in månedsdata[år_måned]:

        if rad[3].strip() == "-" or rad[3].strip() == "":
            continue

        temperatur = float(rad[3].strip().replace(",", "."))

        if temperatur > 20:
            sommerdager[år] += 1

        if temperatur > 25:
            høysommerdager[år] += 1

        if temperatur > 30:
            tropedager[år] += 1


årstall = sorted(sommerdager)

fig2, ax2 = plt.subplots(figsize=(12, 6))

ax2.plot(årstall, [sommerdager[år] for år in årstall],
         label="Sommerdager")

ax2.plot(årstall, [høysommerdager[år] for år in årstall],
         label="Høysommerdager")

ax2.plot(årstall, [tropedager[år] for år in årstall],
         label="Tropedager")

ax2.set_xlabel("År")
ax2.set_ylabel("Antall dager")
ax2.set_title("Sommerdager, høysommerdager og tropedager")
ax2.legend()
ax2.grid(True)

fig2.tight_layout()

# DEL C – GJENNOMSNITTSTEMPERATUR PER ÅR

temperaturer_per_år = {}

for fil in filer:
    with open(fil, "r", encoding="utf-8") as fila:
        leser = csv.reader(fila, delimiter=";")
        next(leser)

        for rad in leser:

            if len(rad) < 5:
                continue

            stasjon = rad[1].strip()

            if not stasjon.startswith("SN"):
                continue

            if rad[2].strip() == "":
                continue

            if rad[4].strip() == "-" or rad[4].strip() == "":
                continue

            try:
                dato = datetime.strptime(rad[2].strip(), "%d.%m.%Y")
                temperatur = float(rad[4].strip().replace(",", "."))
            except ValueError:
                continue

            år = dato.year
            nøkkel = (stasjon, år)

            if nøkkel not in temperaturer_per_år:
                temperaturer_per_år[nøkkel] = {}

            temperaturer_per_år[nøkkel][dato.date()] = temperatur




fig3, ax3 = plt.subplots(figsize=(12, 6))

alle_år = [år for stasjon, år in temperaturer_per_år]
årstall = list(range(min(alle_år), max(alle_år) + 1))

for stasjonsnummer in stasjoner:

    if not stasjonsnummer.startswith("SN"):
        continue

    gjennomsnitt = []

    for år in årstall:

        nøkkel = (stasjonsnummer, år)
        målinger = temperaturer_per_år.get(nøkkel, {})

        if len(målinger) >= 300:
            snitt = sum(målinger.values()) / len(målinger)
            gjennomsnitt.append(snitt)
        else:
            gjennomsnitt.append(float("nan"))

    ax3.plot(årstall, gjennomsnitt,
             label=stasjoner[stasjonsnummer])


ax3.set_title("Gjennomsnittlig årstemperatur")
ax3.set_xlabel("År")
ax3.set_ylabel("Gjennomsnittstemperatur (°C)")
ax3.legend()
ax3.grid(True)

fig3.tight_layout()


vind_per_måned = {}


for måned in range(1, 13):
    vind_per_måned[måned] = []



for år_måned in månedsdata:

    måned = år_måned[1]

    for rad in månedsdata[år_måned]:

        if rad[6].strip() != "-" and rad[6].strip() != "":
            vind = float(rad[6].strip().replace(",", "."))
            vind_per_måned[måned].append(vind)



måneder = []
min_vind = []
median_vind = []
maks_vind = []

for måned in sorted(vind_per_måned):

    målinger = vind_per_måned[måned]

    if målinger:
        måneder.append(måned)

        min_vind.append(min(målinger))
        median_vind.append(median(målinger))
        maks_vind.append(max(målinger))



fig4, ax4 = plt.subplots(figsize=(12, 6))

ax4.plot(måneder, min_vind, marker="o", label="Minimum vindstyrke")
ax4.plot(måneder, median_vind, marker="o", label="Median vindstyrke")
ax4.plot(måneder, maks_vind, marker="o", label="Maksimum vindstyrke")

ax4.set_xlabel("Måned")
ax4.set_ylabel("Vindstyrke (m/s)")
ax4.set_title(f"Vindstatistikk - {stasjoner[stasjon_valg]}")

ax4.set_xticks(range(1, 13))
ax4.legend()
ax4.grid(True)

fig4.tight_layout()


snø_per_sesong = {}

for fil in filer:
    with open(fil, "r", encoding="utf-8") as fila:
        leser = csv.reader(fila, delimiter=";")
        next(leser)

        for rad in leser:

            if len(rad) < 8:
                continue

            stasjon = rad[1].strip()

            if not stasjon.startswith("SN"):
                continue

            if rad[2].strip() in ("", "-"):
                continue

            if rad[7].strip() in ("", "-"):
                continue

            try:
                dato = datetime.strptime(rad[2].strip(), "%d.%m.%Y")
                snødybde = float(rad[7].strip().replace(",", "."))
            except ValueError:
                continue


            if dato.month not in (11, 12, 1, 2, 3, 4):
                continue


            if dato.month >= 11:
                sesong = dato.year
            else:
                sesong = dato.year - 1

            nøkkel = (stasjon, sesong)

            if nøkkel not in snø_per_sesong:
                snø_per_sesong[nøkkel] = {}

            snø_per_sesong[nøkkel][dato.date()] = snødybde



alle_sesonger = sorted(
    {sesong for stasjon, sesong in snø_per_sesong}
)

fig5, ax5 = plt.subplots(figsize=(12, 6))

for stasjon in stasjoner:

    årstall = []
    skidager = []

    for sesong in alle_sesonger:

        nøkkel = (stasjon, sesong)

        målinger = snø_per_sesong.get(nøkkel, {})


        start = datetime(sesong, 11, 1)
        slutt = datetime(sesong + 1, 5, 1)

        antall_dager = (slutt - start).days


        if len(målinger) >= antall_dager / 2:

            antall_skidager = sum(
                1 for snø in målinger.values() if snø >= 20
            )

            årstall.append(sesong)
            skidager.append(antall_skidager)

        else:
            årstall.append(sesong)
            skidager.append(float("nan"))

    if any(verdi == verdi for verdi in skidager):
        ax5.plot(årstall, skidager, label=stasjoner[stasjon])

ax5.set_xlabel("Skisesong (startår)")
ax5.set_ylabel("Antall dager med skiføre")
ax5.set_title("Antall skidager per skisesong")

ax5.legend()
ax5.grid(True)

fig5.tight_layout()

plt.show()