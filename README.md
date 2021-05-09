# Vuoronvaihtosovellus  

## Testaaminen Herokussa
https://tsoha-vuoronvaihtosovellus.herokuapp.com  
* Sovellus toimii parhaiten muilla selaimilla kuin Safarilla tai Internet Explorerilla.
* Sovellusta voi testata Herokussa luomalla uuden käyttäjän.  
* Sovelluksessa on käytössä kaikki listatut toiminnallisuudet.

## Toiminnot

Sovelluksen ideana on mahdollistaa digitaalinen työvuoronvaihto nykyisellä työpaikallani. Työntekijät voivat tarjota vuoroja otettavaksi pois sekä tarjota päiviä, joille voisi ottaa ylimääräisiä vuoroja. Esimies voi hyväksyä tai hylätä vaihtopyyntöjä.  

Ominaisuuksia:  
* Sovellukseen voi kirjautua joko työntekijänä tai esimiehenä.
* Työntekijä näkee eri sivuilta muiden tarjoukset.
* Tarjouksia on kolmea erilaista tyyppiä, ja jokaiselle tyypille on oma sivu:
  1. Vuoro halutaan vaihtaa joko samalle tai eri päivälle toiseen vuoroon.
  2. Vuoro halutaan antaa kokonaan pois.
  3. Otetaan vuoro vastaan jollekin päivälle.
* Esimies näkee kirjautuessaan hyväksyntää odottavat vaihdot.
* Jokaisella sivulla on myös mahdollisuus lisätä listalle oma ehdotus vaihdosta tms.
* Tarjouksista näkyy sovelluksessa erilaisia tietoja sen mukaan mitä tarjotaan:
  * vaihto / pois: pvm, alkamisaika, loppumisaika, työpiste
  * otetaan: pvm
  * lisäksi jokaisella tarjouksella on vapaamuotoinen lisätietokohta, johon työntekijä voi kirjoittaa lisätietoa tarjouksesta
  * tarjoajan nimi
* Vaihtoa / vuoron ottamista / vuoron antamista voi ehdottaa valitsemalla sivun alareunan listasta kyseisen tarjouksen id:n ja täyttämällä lomakkeen.
* Kun vaihtoa ehdottaa, tulee se alkuperäisen ilmoituksen tehneen työntekijän "ehdotukset"-sivulle, josta sen voi hylätä tai hyväksyä. Jos työntekijä hyväksyy ehdotuksen, se katoaa muiden työntekijöiden nähtäviltä ja siirtyy esimiehen hyväksyttäväksi.
* Jos esimies hylkää ehdotuksen, palaa se uudestaan kaikkien nähtäväksi.
* Oman ehdotuksen voi myös poistaa sivun lomakkeella.
* Valitettavasti en saanut csrf-tokenia käyttöön, sillä mikään käyttämistäni selaimista ei toiminut sen kanssa.
