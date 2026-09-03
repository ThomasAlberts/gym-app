# install all backend packages
py -m pip install -r backend/requirements.txt
python -m pip install uv

# run backend
uv run uvicorn backend.main:app --reload  
py -m uv run uvicorn backend.main:app --reload

# Reset db
rm database.db

# Frontend

first run npm install in /frontend

run audit --> run audit fix

npm run dev

fixed
- session time is +2 van echte time
- componenten aangepast en code front-end opgeschoond
- last time moet horizontaal, laatste 3x 

nu
- niet de huidige exercise tonen tijdens het zoeken, of niet de exercise tonen in de exercise als voorgaande
- Bij all exercises opschrijven naam van oefening
- dockerisering van de front/back
- op basis van huidige wokrout advies vragen aan AI 
- mail mij nadat er een account is aangemaakt
- navbar aanpassen, bespreek met anek
- note voor een oefening die je altijd ziet, iets van ques voor je setup, (voeten onder schouders, zit op bankje zet 1 grote stap...)
fix   
- na refresh is niet opgelagen shit ook weg fix of niet?
- fix de components voor de workout pagina, sommige components zijn te groot, select exercise definition die info toont is dezelfde cocde als exercise item die info toont 
- als lijst op dashboard leeg is zeg dat ipv kan niet laden.
- fix homepagina, als niet ingelogd, fix homepage
- de functie oude informatie ophalen aanpassen, nu haalt hij alles op voor het huidige moment, moet zijn voor het moment van de workout, haalt nu dezelfde workout op als oude workout
- pas de notes van vorige keer inzien aan, beetje raar nu
- componenten kleiner vooral workoutsession

latere extra
- instelbare naam over laten gaan, training wk 1, training wk 2??? bekijk hoe
- functie voor het toevoegen van exercise_definition en eventueel movement/ muscle link
of
- de muscle link tonen met plaatjes
- nu gaat na save hij naar /dashboard, misschien later naar een pagina wat totalen van je workout laat zien? en dit eventueel vergelijkt

- op profiel statestieken anders dan dashboard laten zien?
- dashboard in profiel zetten?
- je ziet nu info van de vorige keer dat je een oefening hebt gedaan, laat meerdere keren zien
- workouts van te voren definieren, workouts opslaan voor herbruik later
- export van exercises/workouts

# oude bugs
- na het laten lopen van de timer in set, kan er niet meer gesaved worden of geupdate,
- navbar items worden niet weergegeven op basis van rechten na auth change
