# Vuoronvaihtosovellus  

Sovelluksen ideana on mahdollistaa digitaalinen työvuoronvaihto nykyisellä työpaikallani. Työntekijät voivat tarjota vuoroja otettavaksi pois sekä tarjota päiviä, joille voisi ottaa ylmääräisiä vuoroja. Esimies voi hyväksyä tai hylätä vaihtopyyntöjä.  

Ominaisuuksia:  
* Sovellukseen voi kirjautua joko työntekijänä tai esimiehenä.
* Työntekijä näkee kirjautuessaan muiden tarjoukset.
* Tarjouksia on kolmea erilaista tyyppiä:
  1. Vuoro halutaan vaihtaa joko samalle tai eri päivälle toiseen vuoroon.
  2. Vuoro halutaan antaa kokonaan pois.
  3. Otetaan vuoro vastaan jollekin päivälle.
* Esimies näkee kirjautuessaan hyväksyntää odottavat vaihdot.
* Tarjouksista näkyy sovelluksessa erilaisia tietoja sen mukaan mitä tarjotaan:
  * vaihto / pois: pvm, alkamisaika, loppumisaika, työpiste
  * otetaan: pvm
  * lisäksi jokaisella tarjouksella on vapaamuotoinen lisätietokohta, johon työntekijä voi kirjoittaa lisätietoa tarjouksesta
  * myös tarjoajan nimi näkyy
* Vaihtoa / vuoron ottamista / vuoron antamista voi ehdottaa valitsemalla sivun alareunan listasta kyseisen tarjouksen id:n ja täyttämällä lomakkeen.
* Jos tarjouksen tehneelle kelpaa ehdotus, hän voi hyväksyä sen, jolloin vuoronvaihto siirtyy esimiehen hyväksyttäväksi
* Esimiehen hyväksyntää odottava tarjous katoaa muiden työntekijöiden näkyvistä

## Testaaminen Herokussa
https://tsoha-vuoronvaihtosovellus.herokuapp.com  
* Sovellus toimii parhaiten muilla selaimilla kuin Safarilla tai Internet Explorerilla
* Sovellusta voi tällä hetkellä testata Herokussa luomalla uuden käyttäjän.  
* Sovelluksessa on käytössä kaikki listatut toiminnallisuudet.
