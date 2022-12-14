print(sum([[range(58)[ord(i)-96] for i in b[len(b)//2:] if i in b[0:len(b)//2]][0] for b in open("input.txt").readlines()]))


# zu dokumentationszwecken, ausgeschrieben das obige
print(
    sum(                                            # 9. summe, is klar
        [
            [
                range(58)[ord(i)-96]                # 7. berechne den Wert des Buchstaben nach der Methode unten
                for i                               # 3. für jeden Buchstaben
                in b[len(b)//2:]                    # 4. in der zweiten Hälfte des Rucksacks (// damit eine gerundete ganzzahl rauskommt)
                                                        # sonst hätte ich das \n wegschneiden müssen und int() benutzen müssen
                if i in                             # 5. wenn dieser Buchstabe
                   b[0:len(b)//2]                   # 6. in der ersten Hälfte des rucksacks vorkommt (konvertierung zu set notwendig)
            ][0]                                    # 8. nimm den einzigen wert (garantiert das puzzle)
            for b                                   # 2. für jede zeile
            in open("input.txt").readlines()        # 1. zeilen aus input lesen ['qRQPDqnWFQDtCCBQmQwmGGVG', ...]
        ]
    )
)


# besonders stolz auf die berechnung der alphabetwerte mit rückwärtsindex
# es gibt in python ord, das berechnet den ascii-wert des buchstaben, die sind aber so ein bisschen wild die werte
# (siehe kommentare hier rechts)
offset = 96
print(ord('a'), ord('a') - offset, range(58)[ord('a')-offset])      # 1; ord('a') = 97; -96 = 1
print(ord('z'), ord('z') - offset, range(58)[ord('z')-offset])      # 26; ord('z') = 122; -96 = 26
print(ord('A'), ord('A') - offset, range(58)[ord('A')-offset])      # 27; ord('A') = 65; -96 = -31
print(ord('Z'), ord('Z') - offset, range(58)[ord('Z')-offset])      # 52; ord('Z') = 90; -96 = -6
# range(58) = [0, ..., 58]
# das -31 (also 31-letzte) element ist genau 27 für 'A'
# das -6 (also 6-letzte) element ist genau 52 für 'Z'
# find ich ziemlich elegant ;)
