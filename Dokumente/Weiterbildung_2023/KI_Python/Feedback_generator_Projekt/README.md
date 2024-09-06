# My Project
Dieses Programm extrahiert Keywords aus einer HTML-Seite und generiert mithilfe der OpenAI-API einen Text, der japanischen Lehrern hilft, Feedback-Texte nach dem Unterricht zu verfassen. Um die Qualität der generierten Texte zu optimieren, werden die Daten in MongoDB gespeichert.


# Features
- **Eingabe der Keywords**: Benutzer können über eine HTML-Oberfläche Keywords eingeben.
- **Textgenerierung**: Ein Text wird durch einen Klick auf einen Button in der Benutzeroberfläche generiert.
- **Datenbankintegration**: Die API-Abfragen und die generierten Texte werden in MongoDB gespeichert und chronologisch nach dem Zeitpunkt der Erstellung sortiert angezeigt, wobei die neuesten Einträge zuerst angezeigt werden.
- **Filterung**: Die gespeicherten Daten können nach einer generation-id gefiltert werden.

# TODO
## UI
- Es soll noch eine Funktion implementiert werden, die es ermöglicht, ausgewählte Keywords auf der Benutzeroberfläche zu entfernen.

## Databank


## API-Abfrage
- um die Tokenanzahl der API-Anfragen zu minimieren, soll noch folgendes getestet werden:
    - Beispieltexte aus JSON oder CSV zu lesen, anstatt diese aus Excel zu lesen
- der generierte Text hat noch einen AI-artigen Stil:
    - weitere Tests mit der Anpassung von Temperature- und Promt-Parameter sind notwendig

# Installation
## Vorassetzungen:
- Python 3.x
- MongoDB
- OpenAI-API-Schlüssel





