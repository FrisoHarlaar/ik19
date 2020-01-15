# ik19

Samenvatting <br>
Wij willen een spelletje creëren dat je kan spelen op een browser in de vorm van een trivia spel. Je moet kunnen inloggen zodat je <br>scores kan vergelijken met scores van andere spelers. De scores moeten opgeslagen worden in een database.  Elke speler begint <br>met vier levens die eraf gaan als je een vraag fout of niet binnen de tijd (30 seconden) beantwoordt. Elke vraag geeft één <br>punt, dus elk spel geeft minimaal 4 punten. Er zijn verschillende categorieën en moeilijkheidsgraden.

Features<br> 
4 levens per speler<br> 
Verschillende soorten levels op moeilijkheid (moeilijkere vragen en/of kortere tijd)
Leaderboard waarin de 50 hoogste scores bij worden gehouden.
Aantal categorieën op onderwerp
Timer in de vorm van een klok die veel aandacht trekt, zodat de gebruiker tijdsdruk ervaart. 

Extra:<br> 
Vriendschapsverzoeken om scores met vrienden te vergelijken
Directe versus modus waarbij de laatst overgebleven speler wint
Pop-up met percentage van hoeveel gebruikers die goed hadden geantwoord
Met Javascript geanimeerde error meldingen 

Minimum viable product<br> 
Kunnen registreren, inloggen, uitloggen en je eigen scores bekijken. Een leaderboard met high-scores van andere spelers. Per vraag een timer van 30(?) seconden, als de tijd om is voordat je de vraag hebt beantwoord of als de vraag fout is beantwoord, gaat er een leven van je af. Per vraag krijg je één punt, ongeacht of je de vraag goed of fout hebt, dus met vier levens heb je minimaal vier punten. Errors weergeven door door te verwijzen naar een error pagina, zoals apology in finance.

Afhankelijkheden (plugins) <br> 
Databronnen: API https://opentdb.com/browse.php
Externe componenten: https://getbootstrap.com/ ~ Bootstrap
Concurrerende bestaande: https://www.funtrivia.com/quizzes/
Moeilijkste delen: het werken en animeren met Javascript

Routes<br> 
register: / → register → check (username and password) → index
login: / → login
logout: clear session → /
start game: index → login required → games → choose category/level → start game
highscore board: index → login required → highscores OR index(zie het op index)
index: login → index
Apology: MVP= HTML, anders ideaal=Javascript


![Login sketch](https://raw.githubusercontent.com/Svanmansom/ik19/master/Schetsen/login.png)

![Register sketch](https://raw.githubusercontent.com/Svanmansom/ik19/master/Schetsen/register.png)

![index sketch](https://raw.githubusercontent.com/Svanmansom/ik19/master/Schetsen/index.png)

![dashboard sketch](https://raw.githubusercontent.com/Svanmansom/ik19/master/Schetsen/dashboard.png)

![game sketch](https://raw.githubusercontent.com/Svanmansom/ik19/master/Schetsen/game.png)

![profile sketch](https://raw.githubusercontent.com/Svanmansom/ik19/master/Schetsen/profile.png)

https://drive.google.com/open?id=1i1CcKv4qYAudbn1Wy_uRDpWVmmscqeqm

