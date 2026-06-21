##imports
import re

example_stories = ["Als Endanwender möchte ich mein vergessenes Passwort über einen sicheren Link selbstständig zurücksetzen können, damit ich ohne die Hilfe des IT-Supports schnell wieder Zugriff auf mein Benutzerkonto erhalte und meine Arbeit ohne lange Wartezeiten oder Arbeitsunterbrechungen fortsetzen kann. Die Sicherheit meines Kontos muss dabei jederzeit garantiert bleiben.", "Als Datenanalyst möchte ich die monatlichen Verkaufsberichte mit nur einem Klick als CSV-Datei exportieren können, damit ich die Rohdaten in externen BI-Tools flexibel weiterverarbeiten und visuell aufbereiten kann. Der Export muss alle relevanten Spalten enthalten und darf auch bei großen Datenmengen nicht abstürzen oder blockieren.", "Als Software-Entwickler möchte ich in den Einstellungen der Benutzeroberfläche einen Dark Mode aktivieren können, damit meine Augen bei langen Programmiersitzungen in der Nacht weniger stark ermüden. Das dunkle Design soll für alle Menüs, Editoren und Dialogfenster der Anwendung konsistent übernommen werden und die Lesbarkeit spürbar verbessern.", "Als Sicherheits-Administrator möchte ich, dass alle externen API-Anfragen zwingend ein gültiges OAuth2-Token vorweisen müssen, damit unbefugte Zugriffe auf sensible Kundendaten effektiv verhindert werden. Anfragen ohne ein solches Token oder mit abgelaufenen Zugangsdaten müssen vom System sofort blockiert und mit einer eindeutigen Fehlermeldung abgewiesen werden.", "Als Projekt-Manager möchte ich sofort eine automatische E-Mail-Benachrichtigung erhalten, wenn ein kritisches Ticket im System erstellt oder auf den Status „Blockiert“ gesetzt wird, damit ich sofort reagieren und das Team bei der Problemlösung unterstützen kann. Die E-Mail muss die Ticket-ID und eine Kurzbeschreibung enthalten."]


sdm_repository = {
    "keywords": [
        "datenmodell", "datensatz", "datenstruktur", "datenbank", "tabelle", "spalte", 
        "primärschlüssel", "datentyp", "json", "csv", "xml", "datei", "export", 
        "import", "austauschformat", "parsing", "mapping", "feldzuordnung", "konvertieren", 
        "transformieren", "validierung", "bereinigen", "objekt", "variable", "funktion", 
        "klasse", "backend", "logik", "syntax", "refactoring", "sql", "nosql", 
        "datenqualität", "schema", "migration", "datenstrom", "serialisierung", 
        "deserialisierung", "typisierung", "datenintegrität", "normalisierung", 
        "abfrage", "persistent", "metadaten", "datenfeld", "datenquelle", "datenziel", 
        "datenimport", "datenexport", "datenbereinigung", "speichertyp", "indexierung", 
        "fremdschlüssel", "datenbankschema", "relation", "entität", "attribut", 
        "datensatzid", "array", "string", "integer", "boolean", "float", "nullwert", 
        "datendumping", "datenkonsistenz", "speicherarchitektur", "abfragesprache"
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
        "datenaustausch", "prozesskette", "aufruf", "verbindungsaufbau", "schnittstellenbeschreibung"
    ]
}

gid_repository = { #erstellt ein dictionary
    "keywords": [ #der key "keywords" beeinhaltet eine liste "[...]", mit dne Einträgen nutzer...
        "nutzer", "kunde", "user", "anwender", "endverbraucher", "persona", "zielgruppe", 
        "bedienung", "handhabung", "oberfläche", "frontend", "ui", "ux", "ansicht", "button", 
        "layout", "klick", "dokumentation", "beschreibung", "übergabe", "anleitung", "handbuch", 
        "ticket", "anforderung", "darstellung", "verständlichkeit", "übersicht", "lesbarkeit", 
        "design", "fehlermeldung", "anzeigen", "mockup", "wireframe", "usability", "barrierefreiheit", 
        "farbschema", "navigation", "feedback", "hilfetext", "steuerung", "komponente", 
        "textfeld", "benutzererlebnis", "kundenwunsch", "abnahmekriterien", "release", "schulung", 
        "interaktionsdesign", "grafisch", "oberflächengestaltung", "leserlich", "benutzerführung", 
        "fehlermeldungsdesign", "ansichtsebene", "kundenperspektive", "anwendungsfall"
    ]
}

def regex(keywords_dict):
    keywords = []

    for m in keywords_dict.values():
        keywords.extend(m) #die übergebenen Keywords in "keywords = []" speichern

    #keywords.sort(key=len, reverse=True) #zuerst die langen Wörter finden, bevor die kurzen gefunden werden. Dadurch werde spezifische 

    pattern_string = r"(" + "|".join(keywords) + r")"
    return re.compile(pattern_string, re.IGNORECASE)




def decideSubject(userStory: str) -> str: 
    subjectScoring = {
        "EVP" : 0,
        "GID" : 0,
        "SDM" : 0
    }

    sdm_filter = regex(sdm_repository)
    evp_filter = regex(evp_repository)
    gid_filter = regex(gid_repository)
    

    # re.findall liefert uns eine Liste aller Treffer
    sdm_hits = len(sdm_filter.findall(example_stories[0]))  # Findet: "Validierung", "JSON", "Daten" -> Score: 3
    evp_hits = len(evp_filter.findall(example_stories[0])) # (Über die EVP-Logik) Findet: "REST", "Endpunkt" -> Score: 2
    gid_hits = len(gid_filter.findall(example_stories[0])) # Findet: "Kunde" -> Score: 1


    for m in sdm_repository["keywords"]:
        if m in example_stories[0]:
            subjectScoring["SDM"] += 1
    for m in gid_repository["keywords"]:
        if m in example_stories[0]:
            subjectScoring["GID"] += 1
    for m in evp_repository["keywords"]:
        if m in example_stories[0]:
            subjectScoring["EVP"] += 1

    sortedSubjectScoring = dict(sorted( #dict erstellen und sortieren
        subjectScoring.items(), #Schlüssel-Wert-Paare von subjectScoring nehmenü
        key=lambda x: x[1], #Lambda funktion ist eine Funktion die genau dort definiert wird. Mit x können wir beschreiben, welcher index für die sortierung verwendet werden soll
        reverse=True )) #reverse sorgt für absteigend
    #print("Das Fach EVP hat:", subjectScoring["EVP"] )
    sortedSubjectScoring = list(sortedSubjectScoring.items()) #dictionary in liste umwandeln um einfach ohne weitere Funktionen drauf zuzugreifen

    if(sortedSubjectScoring[0][1] - sortedSubjectScoring[1][1] <= 3) : #wenn wert vom 1. zum 2. weniger als 4 abweicht. Zusätzlich aufnehmen
        print(f"Die Differenz der Keywords vom 2. zum 1. ist kleiner als 4 und wird somit auch als Thema aufgenommen. {sortedSubjectScoring[1][0]} ({sortedSubjectScoring[1][1]}) und {sortedSubjectScoring[0][0]} ({sortedSubjectScoring[0][1]}) ")
        userStory = f"{sortedSubjectScoring[0][0]}, {sortedSubjectScoring[1][0]}"
        print (userStory)
    return userStory


if __name__ == "__main__":
    ergebnis = decideSubject("test")

# User-Story dem Text zuordnen auf UserStory.rolle das Fach hinschreiben




