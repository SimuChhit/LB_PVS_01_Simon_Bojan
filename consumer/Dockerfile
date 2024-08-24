# Wähle ein leichtes Python-Image als Basis
FROM python:3.11-alpine

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Abhängigkeitsdateien in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Consumer-Codes
COPY . .

# Setze den Befehl, der den Consumer startet
CMD ["python", "consumer.py"]
