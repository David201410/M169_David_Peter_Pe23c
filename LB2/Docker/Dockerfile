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