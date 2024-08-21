Ausgangslage und Auftrag
Entwickeln Sie ein verteiltes Finanzsystem welches fiktive Finanzdaten verarbeitet und diese entsprechend abspeichert.
Der Producer welcher synthetische Finanzdaten erzeugt ist als Source Code vorhanden und muss in einen Docker
Container verpackt werden. Weiter sendet er die Daten in ein Message Broker System «RabbitMQ» in verschiedene
Queues um diese dort für die weitere Verarbeitung zwischenzuspeichern. Die Consumer sollen nur jeweils eine
bestimmte Gruppe von Finanzdaten verarbeiten und diese sollen aus einer spezifischen RabbitMQ Queue gelesen
werden. Die Consumer sollen jeweils in 1000er Paketen Daten lesen und daraus den Durchschnitt berechnen und dieses
Resultat danach in eine MongoDB speichern. Die MongoDB soll als Cluster Verbund aufgebaut sein (als Replicaset) sodass
eine Ausfallsicherheit gewährleistet werden kann. Weiter sollen die aggregierten Finanzdaten über ein «Frontend»
einsehbar sein welches auch als Source Code zur Verfügung gestellt wird und in einen Docker Container verpackt werden
soll. Auch das Frontend soll ausfallsicher gestaltet werden und soll daher aus mindestens 2 Instanzen bestehen mit einem
Load Balancer, der die Anfragen auf die Systeme verteilt.Parallele und verteilte Systeme
13.08.2024 3 / 5 Patrick Michel
Komponenten
Nachfolgend werden die einzelnen Komponenten des verteilten Systems beschrieben und welche Funktion diese jeweils
erfüllen.
Producer «Stock-Publisher»
• Produziert zufällige «Buy» & «Sale» Datenpakete welche Finanztransaktionen auf einem Finanzmarkt von einer
bestimmten Firma widerspiegeln sollen.
• Wird als Golang Applikation zur Verfügung gestellt.
o Code: https://github.com/SwitzerChees/stock-publisher
o Aufgabe: Dieser Producer soll in ein Container Image verpackt werden, sodass er in eine Docker Compose
Umgebung integriert werden kann.
o Aufgabe: Weiter soll das gebaute Image auf Docker Hub veröffentlicht werden.
Rabbit MQ «Message Broker»
• Dient als Zwischenspeicher zwischen Producer und Consumer und hält die vom Producer generierten Datenpakete in
Queues.
o Aufgabe: Soll als Container in eine Docker Compose Umgebung integriert werden, sodass dieser vom
Producer Datenpakete empfangen kann
o Aufgabe: Soll auch mit dem Consumer verbunden werden, sodass die Datenpakete weiterverarbeitet
werden können.
Consumer
• Konsumiert die vom Producer generierten Datenpakete aus der RabbitMQ Queue und aggregiert diese sodass daraus
der Durchschnitt des Preises berechnet werden kann. Das Resultat soll danach in eine MongoDB gespeichert werden.
o Aufgabe: Erstellen Sie mit einer Programmiersprache Ihrer Wahl ein kleines Programm, welches in der Lage
ist Nachrichten von einer spezifischen RabbitMQ Queue zu lesen (jeweils 1000 Stück), diese zu aggregieren
und das Ergebnis in eine MongoDB Collection zu speichern.
o Aufgabe: Die Connection Strings für die RabbitMQ und MongoDB sowie die spezifische Queue soll über
Umgebungsvariablen gesteuert werden können
o Aufgabe: Verpacken Sie das Programm in ein Container Image, sodass er in eine Docker Compose
Umgebung integriert werden kann. Das Image soll auf Docker Hub veröffentlicht werden.
MongoDB Cluster
• Dient als Ausfallsicheres Speichersystem um die Resultate des Consumers redundant zu speichern.
o Aufgabe: Soll als Container in eine Docker Compose Umgebung integriert werden, sodass dieser vom
Consumer die Resultate empfangen kann.
o Aufgabe: Soll auch mit dem Frontend verbunden werden, sodass die Resultate angezeigt werden können.
Frontend «Stock-Liveview»
• Zeigt die Resultate, welche in die MongoDB gespeichert werden als Livestream an.
• Wird als NodeJS Applikation zur Verfügung gestellt.
o Code: https://github.com/SwitzerChees/stock-liveview
o Aufgabe: Dieses Frontend soll in ein Container Image verpackt werden, sodass er in eine Docker Compose
Umgebung integriert werden kann.
o Aufgabe: Weiter soll das gebaute Image auf Docker Hub veröffentlicht werden.
NGINX «Load Balancer»
• Dient als Lastverteilung und als Failover für das Frontend.
o Aufgabe: Soll als Container in eine Docker Compose Umgebung integriert werden, sodass dieser mit den
Frontends kommunizieren kann.
o Aufgabe: Soll die Anfragen auf mindestens 2 Frontends verteilten und bei einem Ausfall ein sauberes
Failover machen
