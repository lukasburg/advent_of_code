print(max([sum([int(n) for n in backpack.split("\n")]) for backpack in open(
    "puzzles-input.txt").read().strip().split("\n\n")]))
print(sum(sorted([sum([int(n) for n in backpack.split("\n")]) for backpack in open(
    "puzzles-input.txt").read().strip().split("\n\n")], reverse=True)[0:3]))

## Erklärung 1:
# Von innen nach außen entsprechend der Nummern läuft python durch
print(                                      # 13. Zum Schluss gib das Ergebnis aus
    max(                                    # 12. Finde das maximum in 11 (praktischer Helfer)
        [
            sum(                            # 10. Bilde die Summe aller Werte der Liste (praktischer Helfer)
                [
                    int(n)                  # 8. Konvertiere den string ('123') in eine Zahl (123)
                    for n in                # 7. für jeden Wert tue das obige
                    backpack.split("\n")    # 6. teile den Rucksack ('123\n3543') an seinen Zeilenumbrüchen
                                                # heraus kommt: ['123', '3543']
                ]                           # 9. heraus kommt: [123, 3543]
            )
            for backpack in                 # 5. für jeden string in dieser Liste tu das oben

            open("puzzles-input.txt")       # 1. öffne die datei
                .read()                     # 2. lies den gesamten Inhalt aus
                .strip()                    # 3. Entferne überschüssige leerzeichen am Ende (und anfang)
                .split("\n\n")              # 4. Trenne den Inhalt an den Stellen mit zwei Zeilenumbrüchen hintereinander
                                                # also dort wo ein Rucksack aufhört
                                                # raus kommt eine Liste mit strings, die die Rucksäcke der Elfen repräsentieren
                                                # ['123\n3543', '156', '43\n3546']
                                                # ( '\n' als zeichen für ursprünglichen zeilenumbruch)

        ]                                   # 11. Heraus kommt eine Liste an Rucksacksummen [3666, 156, 3599]
    )
)

# Erklärung 2:
print(
    sum(                # 5. Und bildet die Summe der höchsten drei
        sorted(         # 2. Sortiere die Liste, von höchstem zu niedrigstem (siehe 3)
            # 1. Wie oben gleiche List an Rucksackwerten (siehe 10 & 11)
            [sum([int(n) for n in backpack.split("\n")]) for backpack in open(
                "puzzles-input.txt").read().strip().split("\n\n")]
            , reverse=True      # 3. von hoch zu niedrig
        )
            [0:3]               # 4. Sogenanntes Slicing (ist etwas mehr, aber gibts gute tutorials und ist ein feature
                                #   was ich bisher nur aus python kenne.
                                # nimmt nur die ersten drei Werte (Der nullte bis (ohne) der dritte Wert)
    )
)
