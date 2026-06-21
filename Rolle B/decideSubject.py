##imports
import re

example_stories = ["Als Endanwender möchte ich mein vergessenes Passwort über einen sicheren Link selbstständig zurücksetzen können, damit ich ohne die Hilfe des IT-Supports schnell wieder Zugriff auf mein Benutzerkonto erhalte und meine Arbeit ohne lange Wartezeiten oder Arbeitsunterbrechungen fortsetzen kann. Die Sicherheit meines Kontos muss dabei jederzeit garantiert bleiben.", "Als Datenanalyst möchte ich die monatlichen Verkaufsberichte mit nur einem Klick als CSV-Datei exportieren können, damit ich die Rohdaten in externen BI-Tools flexibel weiterverarbeiten und visuell aufbereiten kann. Der Export muss alle relevanten Spalten enthalten und darf auch bei großen Datenmengen nicht abstürzen oder blockieren.", "Als Software-Entwickler möchte ich in den Einstellungen der Benutzeroberfläche einen Dark Mode aktivieren können, damit meine Augen bei langen Programmiersitzungen in der Nacht weniger stark ermüden. Das dunkle Design soll für alle Menüs, Editoren und Dialogfenster der Anwendung konsistent übernommen werden und die Lesbarkeit spürbar verbessern.", "Als Sicherheits-Administrator möchte ich, dass alle externen API-Anfragen zwingend ein gültiges OAuth2-Token vorweisen müssen, damit unbefugte Zugriffe auf sensible Kundendaten effektiv verhindert werden. Anfragen ohne ein solches Token oder mit abgelaufenen Zugangsdaten müssen vom System sofort blockiert und mit einer eindeutigen Fehlermeldung abgewiesen werden.", "Als Projekt-Manager möchte ich sofort eine automatische E-Mail-Benachrichtigung erhalten, wenn ein kritisches Ticket im System erstellt oder auf den Status „Blockiert“ gesetzt wird, damit ich sofort reagieren und das Team bei der Problemlösung unterstützen kann. Die E-Mail muss die Ticket-ID und eine Kurzbeschreibung enthalten."]

NAME = 0
NUMBERVALUE = 1

sdm_repository = {
    "keywords": [
        "datenmodell", "datensatz", "datenstruktur", "datenbank", "tabelle", "spalte", 
        "primärschlüssel", "fremdschlüssel", "datentyp", "json", "csv", "xml", "datei", 
        "export", "import", "austauschformat", "parsing", "mapping", "feldzuordnung", 
        "konvertieren", "transformieren", "validierung", "bereinigen", "objekt", 
        "variable", "funktion", "klasse", "backend", "logik", "syntax", "refactoring", 
        "sql", "nosql", "datenqualität", "schema", "migration", "datenstrom", 
        "serialisierung", "deserialisierung", "typisierung", "datenintegrität", 
        "normalisierung", "abfrage", "persistent", "metadaten", "datenfeld", 
        "datenquelle", "datenziel", "datenimport", "datenexport", "datenbereinigung", 
        "speichertyp", "indexierung", "datenbankschema", "relation", "entität", 
        "attribut", "datensatzid", "array", "string", "integer", "boolean", "float", 
        "nullwert", "datendumping", "datenkonsistenz", "speicherarchitektur", 
        "abfragesprache", "datenverarbeitung", "objekterstellung", "instanziierung",
        "anwendungsstruktur", "ablauflogik", "kontrollstruktur", "quellcode", 
        "speicherort", "datenflussdiagramm", "datenvalidierung", "wertzuweisung"
    ]
}

evp_repository = {
    "keywords": [
        "api", "rest", "webhook", "schnittstelle", "endpoint", "endpunkt", "grpc", "soap", 
        "anfrage", "antwort", "request", "response", "payload", "http", "statuscode", "post", 
        "get", "workflow", "integration", "weiterverarbeitung", "automatisierung", "pipeline", 
        "datenfluss", "trigger", "server", "client", "middleware", "authentifizierung", 
        "token", "vernetzung", "nachrichtenschlange", "oauth", "header", "ssl", "tls", 
        "handshaking", "routing", "gateway", "proxy", "microservice", "pubsub", "mqtt", 
        "amqp", "verbindung", "timeout", "retry", "netzwerk", "port", "ipadresse", "websockets", 
        "kommunikationsprotokoll", "datenübertragung", "systemübergreifend", "nachrichtenbus", 
        "datenaustausch", "prozesskette", "aufruf", "verbindungsaufbau", "prozessfluss",
        "schnittstellenbeschreibung", "systemintegration", "dateneingang", "datenausgang",
        "übergangsautomatisierung", "nachrichtenübermittlung", "remoteproduzedurecall"
    ]
}

gid_repository = { 
    "keywords": [ 
        "nutzer", "kunde", "user", "anwender", "endverbraucher", "persona", "zielgruppe", 
        "bedienung", "handhabung", "oberfläche", "frontend", "ui", "ux", "ansicht", "button", 
        "layout", "klick", "dokumentation", "beschreibung", "übergabe", "anleitung", "handbuch", 
        "ticket", "anforderung", "darstellung", "verständlichkeit", "übersicht", "lesbarkeit", 
        "design", "fehlermeldung", "anzeigen", "mockup", "wireframe", "usability", "barrierefreiheit", 
        "farbschema", "navigation", "feedback", "hilfetext", "steuerung", "komponente", 
        "textfeld", "benutzererlebnis", "kundenwunsch", "abnahmekriterien", "release", "schulung", 
        "interaktionsdesign", "grafisch", "oberflächengestaltung", "leserlich", "benutzerführung", 
        "fehlermeldungsdesign", "ansichtsebene", "kundenperspektive", "ergebnisdarstellung",
        "anwendungsfall", "nutzerzentriert", "bedienungskomfort", "projektdokumentation"
    ]
}

def regex(keywords_dict):
    keywords = []

    for m in keywords_dict.values():
        keywords.extend(m) #die übergebenen Keywords in "keywords = []" speichern

    keywords.sort(key=len, reverse=True) #zuerst die langen Wörter finden, bevor die kurzen gefunden werden. Dadurch werden die Wörter nicht abgeschnitten.
    pattern_string = r"\b(" + "|".join(keywords) + r")\b"
    return re.compile(pattern_string, re.IGNORECASE)



def decideSubject(userStory: str) -> str: #gibt einen String mit den Fächern zurück, sollte es keine Übereinstimmung geben wird "null" als string zurückgegeben
    subjectScoring = {
        "EVP" : 0,
        "GID" : 0,
        "SDM" : 0
    }

    sdm_filter = regex(sdm_repository)
    evp_filter = regex(evp_repository)
    gid_filter = regex(gid_repository)

    # dictionary beschreiben
    subjectScoring["SDM"] = len(sdm_filter.findall(userStory))  
    subjectScoring["EVP"] = len(evp_filter.findall(userStory)) 
    subjectScoring["GID"] = len(gid_filter.findall(userStory)) 


    sortedSubjectScoring = dict(sorted( #dict erstellen und sortieren
        subjectScoring.items(), #Schlüssel-Wert-Paare von subjectScoring nehmenü
        key=lambda x: x[1], #Lambda funktion ist eine Funktion die genau dort definiert wird. Mit x können wir beschreiben, welcher index für die sortierung verwendet werden soll
        reverse=True )) #reverse sorgt für absteigend
    #print("Das Fach EVP hat:", subjectScoring["EVP"] )
    sortedSubjectScoring = list(sortedSubjectScoring.items()) #dictionary in liste umwandeln um einfach ohne weitere Funktionen drauf zuzugreifen

    firstSubject = sortedSubjectScoring[0]
    secondSubject = sortedSubjectScoring[1]
    thirdSubject = sortedSubjectScoring[2]

    if(firstSubject[NUMBERVALUE] - secondSubject[NUMBERVALUE] <= 3 and secondSubject[NUMBERVALUE] != 0) : #wenn wert vom 1. zum 2. weniger als 4 abweicht. Zusätzlich aufnehmen
        subjects = f"{firstSubject[NAME]}, {secondSubject[NAME]}"
        if(firstSubject[NUMBERVALUE] - thirdSubject[NUMBERVALUE] <= 3 and thirdSubject[NUMBERVALUE] != 0) : #wenn der Wert vom 1. zum 3. um weniger als 4 abweicht, auch das Thema zuweisen
            subjects = f"{firstSubject[NAME]}, {secondSubject[NAME]}, {thirdSubject[NAME]} "
    elif(firstSubject[NUMBERVALUE] >= 1):
        subjects = f"{firstSubject[NAME]}"
    else:
        subjects = "null"
    
    return subjects

"""
if __name__ == "__main__":
    # Test-Schleife über alle Beispiel-Stories
    for i, story in enumerate(example_stories):
        print(f"\n--- Analysiere Story {i+1} ---")
        ergebnis = decideSubject(story)
        print(f"Zugeordnetes Fach / Fächer: {ergebnis}")
"""
# User-Story dem Text zuordnen auf UserStory.rolle das Fach hinschreiben




