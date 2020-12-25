# boxhead-2play
Indaplus20 task 13 &amp; 14 multiplayer spel inspirerat av [boxhead 2play](https://www.crazygames.se/spel/boxhead-2play-rooms)!

Skapad av [@alaad](https://gits-15.sys.kth.se/alaad) och [@nilszen](https://gits-15.sys.kth.se/nilszen).

[Ersode repo](https://gits-15.sys.kth.se/ersode/indaplus20/tree/master/task-13-14).

### Hur kör man?
I en terminal, kör `python3 server.py` för att starta servern.

Kör sedan `python3 client.py` i två andra terminaler för att få två spelare som man kan styra med piltangenterna!

## Information och krav
Ni har redan blivit indelade i grupper. Om du ej blivit indelad, och ångrat dig och vill vara med i ett projekt, PMa mig på Discord ASAP.

Uppgiften är att skapa ett spel med multiplayer-capabilities och grafik. Börja med detta:

1. Lägg till varandra på Discord (gå till members list i Discord och hitta er partner) så att ni enkelt kan chatta och screensharea med varandra.
2. Skapa ett privat repository på gits, och [lägg till _både er partner och mig (ersode)_ som collaborators.](https://i.imgur.com/xlfjweA.gif)
3. Lägg en länk till repot längst upp i ert vanliga week-13 repo. 
4. Skapa ett delat google-dokument där ni kan lägga in idéer medan ni brainstormar (dela ej dokumentet med mig).
5. Bestäm tillsammans ett programmeringsspråk som ni vill använda. Kolla gärna upp redan innan vilka alternativ det finns för grafik och hur man hanterar nätverkskommunikation.
6. Bestäm en spelidé.

Krav på spelet:
* Det ska finnas flera maps/kartor/banor. Det är inte ett krav att kartorna ska kunna ändras mid-round, men spelsessionen ska heller inte behöva startas om helt.
* Spelare ska kunna röra på sig i spelvärlden, med collision.
* Det ska finnas föremål synliga på mappen som spelare kan plocka upp och användas. Ett upplockat föremål ska försvinna från spelvärlden, och istället synas i spelarens inventory.
* Ett interface - kraven här är ganska låga, men lämpligt är väl åtminstone en meny innan man connectar, och någon form av inventory väl inne i spelet.
* Det ska finnas NPCs av någon typ 
    * Här säger vi att en NPC är något som kan röra sig, som ej är en spelare, som på något sätt kan spawna och despawna, och som har någon form av extremt enkel AI som rör sig "oförutsägbart", dvs dess rörelse ska inte vara hårdkodad på klienternas sida. Den ska även gå att ha någon form av interaktion med.
* Objekt såsom spelare, föremål, statistik (HP?) etc. ska givetvis alltid vara synkroniserade.
* En klient får vara "authoritative", dvs. agerar server, och bestämmer alltså vad som "får" hända; spelarrörelse (movement) och statistik såsom HP eller damage får ej kunna "fuskas".
    * Skicka vad klienter försöker göra, och låt servern bestämma vad som händer.
        * Exempel på bra command: "Rörelse i höger riktning"
        * Exempel på dåligt command: "Jag (Spelare 5) rör mig till koordinater x,y"
    * I övrigt behöver ni inte skydda er från diverse mindre självklara fusk (såsom hit detection), men det ska **absolut inte** gå att exekvera arbiträr kod på den andres dator (t.ex. via `eval`.)
* Det är inte acceptabelt att i varje uppdatering skicka hela spelplanen med alla positioner, utan uppdateringar ska vara kumulativa.
* Kommunikationen ska vara någorlunda effektiv (inte JSON), och vara skriven på ett sätt som inte är exklusivt för ett visst programmeringsspråk (inte pickle). Det är okej att använda ett serialiseringsbibliotek.
* Riktiga programmeringsspråk och riktiga sockets. Inte någon spelmotor (Unity), inget som abstraherar bort sockets (Websockets). Inget Javascript eller liknande.
* Koden ska vara väldokumenterad med kommentarer.


Fokuset är att synkronisera saker över nätverket, inte att grafiken ska se bra ut eller ha jättemånga olika features. TCP rekommenderas. Flertrådad programmering är inte ett krav, men kanske kan underlätta beroende på valt språk.

Diskutera regelbundet vad ni gör/gjort, committa ofta, visa varandra kod ni skrivit och förklara den. Parprogrammera gärna! Båda ska kunna redovisa all kod i projektet.

## Krav till första övningen:
* Exercise I.1 (vanlig uppgift) ska göras och lämnas in individuellt.
* Ni ska ha fått igång grafik och movement så att ni åtminstone har synkade spelarpositioner och rörelse. Det gör inte så mycket om ni inte har andra features vid det laget.
