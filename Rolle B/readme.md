# Rolle B

### Ich hatte die Aufgabe eine Funktion zu schreiben, die eine Userstory einliest und anschließend bewertet ob es zu GID, SDM oder EVP gehört.

Die Umsetzung erfolgte durch ein Bewertungssystem, welches für jedes fachbezogene Keyword, den Score des Faches um 1 erhöht. Das finden der Keywords wurde mit RegEx bzw. dem Modul `re` aus Python implementiert. 

Die Möglichkeit, dass mehrere Fächer einer Userstory zugeordnet werden, wurde so umgesetzt, dass sobald das 2. Höchstbewerteste Fach innerhalb von 3 Punkten des 1. Bewertesten fach's liegt, das dann dies zusätzlich zu dem Fach zugeordnet wird. Dasselbe gilt für den 2. und 3. platziertes Fach.

Beispiel: 

EVP(7), GID(5), SDM(1)

Hier hat GID einen Abstand von 2 Punkten zu EVP, somit wird die Userstory den Fächern EVP und GID zugeordnet. SDM liegt mehr als 3 Punkte hinter GID und wird somit nicht weiter berücksichtigt.

Um die Funktion zu testen wurden KI-generierte Userstorys verwendet und evaluiert. Beim testen hat sich herausgestellt, dass die Kriterien an die Software erfüllt wurden und die Fächer entsprechend zugeordnet werden.

Die Funktion `decideSubject(userStory: str) -> str:` erwartet einen String, welcher die Userstory beeinhaltet und gibt die Fächer z.B `GID, SDM` als String zurück. 