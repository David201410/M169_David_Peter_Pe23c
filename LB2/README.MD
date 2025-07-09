# Projekt LB2: Containerisierte To-Do-(web)Anwendung

## Inhaltsverzeichnis
1. Einleitung
2. Service-Beschreibung
3. Projektstruktur
4. Umsetzung
    - app.py
    - requirements.txt
    - Dockerfile
    - docker-compose.yml
5. Containerisierung & Deployment
6. Bedienung & Benutzeroberfläche
7. Optimierungspotenzial
8. Quellen

## Einleitung
In diesem Projekt wurde eine einfache To-Do-Anwendung containerisiert. Ziel war es, eine mehrschichtige Web-Applikation in einem Container-Setup mit Flask, SQLite und Docker Compose umzusetzen, sowie die Konzepte der Containerisierung und serviceorientierter Architektur praktisch anzuwenden.

Als Grundlage für meine Arbeit habe ich eine EC2 Instanz (Ubuntu) aufgesetzt und darauf mein Dockerprojekt erarbeitet. Im grossen und ganzen ist es nicht sehr komplex.

Jedoch bietet meine LB2 eine gute Grundlage für eine Webanwendung die sich leicht über docker-compose deployen lässt. Selbstverständlich könnte man mehr Container daraus machen, mein Fokus lag aber mehr darauf, etwas für mich kompaktes zu machen.


## Ziele
Implementierung einer einfachen Web-Applikation zur Verwaltung von Aufgaben

- Persistente Speicherung in einer SQLite-Datenbank
- Containerisierung in separaten Services für Web-App und Datenvolumen
- Einfache Bedienung und schneller Start via Docker Compose


## Service-Beschreibung
Die To-Do-Anwendung ermöglicht es Benutzern, Aufgaben anzulegen, als erledigt zu markieren und zu löschen. Sie dient als Minimalbeispiel für CRUD-Funktionalität (Create, Read, Update, Delete) und demonstriert:

- Persistente Datenspeicherung mittels SQLite und SQLAlchemy

- Web-basierte Benutzeroberfläche mit Flask und Jinja2

- Container-basiertes Deployment mit Docker und Docker Compose


## Projektstruktur

```
projekt-root/
├── app.py                 # Hauptapplikation (Flask)
├── requirements.txt       # Abhängigkeiten-Definition (Versionsdefinierungen)
├── Dockerfile             # Image-Build-Anweisungen
├── docker-compose.yml     # Orchestrierung der Container
├── db/
│   └── db.sqlite          # Persistente SQLite-Datenbank (Volume)
└── templates/
    ├── base.html          # Haupt-Template mit Formular und Liste
```

## Komponenten & Funktionsweise

### app.py
**Beschreibung**: Steuerung der HTTP-Routen und Datenbankinteraktion via Flask und SQLAlchemy.

```
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.create_all() 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(1000), nullable=False)
    complete = db.Column(db.Boolean) 
    user_id = db.Column(db.Integer)

@app.route('/')
def index():
    todoList = Todo.query.all()
    return render_template('base.html', todo_list=todoList)

# Task hinzufügen
@app.route('/add', methods=["POST"])
def add():
    # Tasknamen aus dem Formular holen
    title = request.form.get("title")
    # Wenn der Titel leer ist, zurück zur Startseite
    if title == "":
        return redirect(url_for("index"))
    # Erstelle ein neues Todo-Objekt
    newTask = Todo(task=title, complete=False)
    # Versuche, das Objekt in die Datenbank hinzuzufügen
    try:
        db.session.add(newTask)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Es gab ein Problem beim erstellen des Tasks."

# einen task löschen
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # den task in der Datenbank suchen
    task = Todo.query.filter_by(id=todo_id).first()
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Task kann nicht gelöscht werden."

# task löschen
@app.route('/update/<int:todo_id>')
def update(todo_id):
    # den task in der Datenbank suchen
    task = Todo.query.filter_by(id=todo_id).first()
    # toggle the complete value
    task.complete = not task.complete
    # versuche in die db zu schreiben
    try:
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Task kann nicht gelöscht werden."

if __name__ == "__main__":
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)
```

### requirements.txt
Alle benötigten Bibliotheken:

```
Flask>=1.1.2
Flask-SQLAlchemy>=2.5.1
gunicorn>=20.1.0
```

### Dockerfile

```
FROM python:3.10-slim

# Arbeitsverzeichnis im Container 
WORKDIR /app

# requirements werden in den Container kopiert
COPY requirements.txt .

# mit pip werden automatisch die requirements heruntergeladen
RUN pip install --no-cache-dir -r requirements.txt

# restlichen code in den Container Rootverzeichnis kopieren
COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
CMD ["python", "app.py"]
```

### docker-compose.yml

```
services:
  app:
    image: ghcr.io/david201410/todolist-davpet:latest
    build: .
    ports:
      - 80:5000
    volumes:
      - todolist.db:/app/db
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1 # Kann weggelassen werden

volumes:
  todolist.db:
    name: todolist_db
```

Die restlichen Files (DB-Datei & html-template) finden sich übrigens im Projektordner **Docker**. 


## Containerisierung & Deployment
1. **Image bauen:** docker build -t ghcr.io/david201410/todolist-davpet:latest .
![image](/LB2/images/01_docker_build.png)

2. **Container starten:** docker run -d --name todo-app -p 80:5000 ghcr.io/david201410/todolist-davpet:latest
![image](/LB2/images/02_docker_run.png)

Es funktioniert!
![image](/LB2/images/03_webseite_lauft.png)

3. **Logs prüfen** docker logs -f todo-app
![iamge](/LB2/images/04_docker_logs.png)

Und das Log nach Eingaben:
![image](/LB2/images/05_docker_logs_after.png)


## Bedienung & Benutzeroberfläche
- **Startseite:** Alle To-Dos werden chronologisch angezeigt.
- **Aufgabe hinzufügen:** Eingabe über Formular, Validierung von Leerwerten.
- **Erledigen/Ungesehen:** Toggle-Button neben jedem Item.
- **Löschen:** Lösch-Icon entfernt Eintrag nach Bestätigung.

**Positiv** Durch das Volume und der darinliegenden SQLLite DB sind die Dateien persistent gespeichert. 


## Optimierungspotenzial

- User-Authentifizierung: Anmeldung und persönliche Listen.
- REST-API: Ausbau mit JSON-Endpunkten für externen Zugriff.
- Styling: Einbindung von Bootstrap oder Tailwind CSS.
- Tests: Unit- und Integrationstests mit pytest und Flask-Testing.

## Quellen

- [https://github.com/patrickloeber/flask-todo](https://github.com/patrickloeber/flask-todo)
- [https://www.python-engineer.com/posts/flask-todo-app/](https://www.python-engineer.com/posts/flask-todo-app/)
- [https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)
- (Fehlerbehebung) [https://stackoverflow.com/questions/77697331/how-to-automatically-create-a-database-with-flask](https://stackoverflow.com/questions/77697331/how-to-automatically-create-a-database-with-flask)
- [https://www.python-engineer.com/posts/flask-todo-app/](https://www.python-engineer.com/posts/flask-todo-app/)
- [https://flask.palletsprojects.com/en/stable/tutorial/templates/](https://flask.palletsprojects.com/en/stable/tutorial/templates/)