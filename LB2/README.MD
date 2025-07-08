## Einführung
In diesem Projekt wird eine To-do-Webanwendung entwickelt, die in einem Docker-Container läuft und auf AWS bereitgestellt wird. Diese Dokumentation umfasst die Planung und Umsetzung eines containerisierten Dienstes. Zur Verwaltung und Bereitstellung der Docker-Images verwende ich wie bisher meine Container-Registry ghcr.io. Die Anwendung soll alle geforderten Teilaufgaben (u. a. zu Monitoring und Security) integrieren. In dieser Dokumentation werden die Schritte von der Entwicklung der Anwendung bis zum Deployment auf AWS Schritt für Schritt erläutert, einschliesslich der Einführung von Logging/Monitoring und Sicherheitsaspekten.

## Projektüberblick
Die gewählte Anwendung ist eine einfache To-do-Liste als Web-App. Die Benutzer sollen Aufgaben erstellen, anzeigen, abhaken und löschen können. Die Umsetzung kann beispielsweise mit einem Node.js-Backend (Express.js) und einem simplen Frontend (HTML/CSS/JavaScript oder ein leichtgewichtiges Framework) erfolgen. Zur Vereinfachung werden die Aufgaben in einer lokalen Datei oder In-Memory gespeichert (für einen produktiven Einsatz wäre eine externe Datenbank ratsam, was das Projekt jedoch komplexer machen würde). 


Die Hauptfunktionalität der App ist das CRUD (Create, Read, Update, Delete) von To-do-Einträgen über eine Weboberfläche oder eine REST-API. Durch die Containerisierung ist sichergestellt, dass die Anwendung mit all ihren Abhängigkeiten in einem Docker-Image gekapselt ist. Dadurch kann sie konsistent auf verschiedenen Umgebungen laufen. 


Als Hosting-Plattform wird AWS EC2 genutzt: Eine virtuelle Linux-Instanz dient als Docker-Host, auf dem der To-Do-Container läuft. Die Docker-Images werden in der GitHub Container Registry (ghcr.io) gespeichert. Mithilfe dieses Workflows kann der Container beispielsweise von GitHub Actions gebaut und in die Registry gepusht werden. Anschliessend zieht sich die AWS-Instanz das Image von dort.

## Architektur
Die Architektur der Lösung ist relativ einfach gehalten:

- **Client (Browser)**: Greift über HTTP/S auf die Webanwendung zu (z.B. via öffentliche IP oder Domain der EC2-Instanz).
- **Webanwendung (Docker-Container)**: Enthält den Webserver mit der To-Do-App. Der Container lauscht auf einem Port (z.B. 5001) für HTTP-Anfragen.
- **Docker-Host (AWS EC2)**: Linux-VM in AWS, auf der Docker Engine installiert ist. Diese Instanz hostet den Container. Sicherheitsgruppen der Instanz sind so    konfiguriert, dass der benötigte Port (z.B. oder 5001) von aussen erreichbar ist.
- **Container Registry (ghcr.io)**: Zentrale Registry, in die das Docker-Image der Anwendung hochgeladen wird. Von hier kann die EC2-Instanz (und auch andere Hosts) das Image herunterladen. Zugriff erfordert Authentifizierung mittels eines Tokens.
- **Optional (falls genügend Zeit Vorhanden)**: Datenpersistenz: Für dieses Projekt speichern wir Daten lokal (im Container-Dateisystem oder in-memory). In einer erweiterten Architektur könnte ein externer Datenbank-Service (z.B. AWS RDS für MySQL/Postgres oder MongoDB Atlas) angebunden werden. Das würde dann per Netzwerk von der Anwendung aus angesprochen und die Zugangsdaten sicher als Umgebungsvariablen im Container hinterlegt.

**Architekturdiagramm**


docker run -d -p 5001:5000 -v todolist.db:/app/db ghcr.io/david201410/todolist-davpet:v2