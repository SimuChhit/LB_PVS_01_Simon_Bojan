# Use the official Node.js image as the base image
FROM node:22

# Arbeitsverzeichnis im Container erstellen und setzen
WORKDIR /app

# Kopiere die package.json und package-lock.json (falls vorhanden)
COPY package*.json ./

# Installiere die Abhängigkeiten
RUN npm install

# Kopiere den Rest der Applikation ins Arbeitsverzeichnis
COPY . .

# Setze die Umgebungsvariable für den Port
ENV PORT=3000

# Exponiere den Port, auf dem die App läuft
EXPOSE 3000

# Startbefehl für die Anwendung
CMD ["node", "app.js"]
