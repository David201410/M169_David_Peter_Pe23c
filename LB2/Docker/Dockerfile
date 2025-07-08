FROM python:3.8-slim-buster 

WORKDIR /

# environment variabeln für die app
ENV FLASK_APP app.py
ENV FLASK_ENV development

# requirements werden in den Container kopiert
COPY ./requirements.txt /requirements.txt

# mit pip3 werden automatisch die requirements heruntergeladen
RUN pip3 install -r requirements.txt

RUN mkdir app
WORKDIR /app

# projektdateien ins Container Rootverzeichnis kopieren
COPY . .

# app im Container ausführen 
CMD python3 app.py
