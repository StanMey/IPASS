# IPASS project
## Formaticx
Formatixc is een library om formaties tegenover elkaar uit te zetten
om zo de effectiefste tegenformatie te vinden voor elke formatie.  

### Repository
De repository bevat de code, applicatie en documentatie van het IPASS-project.
De library bevindt zich onder `Recommendation_lib/`.
Iedere functie en class bevat documentatie en een overzicht van al deze
documentatie kan gevonden worden onder `pydoc_documenation/`.

### Applicatie
De webapplicatie bevindt zich onder `Application/`.
De applicatie is ontwikkeld met behulp van Flask. Om de applicatie te starten
moet `app.py` gerunned worden.

### Library
Om de library te gebruiken moet er een object van de klasse LeagueRecom
geïnstantieerd worden. Deze klasse vereist een lijst van objecten van de klasse Game en
een lijst met objecten van de klasse Ranking.
Ook moeten de punten gegeven worden die een formatie krijgt wanneer er gewonnen wordt of bij een gelijkspel.  
Hierna kan op het aangemaakte object de functie `create_league_recom()` aangeroepen worden.
De aanbevelingen worden dan gecreeërd.
