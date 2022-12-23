# Vuoden-Harmain-Sovellus
[Backlog](https://docs.google.com/document/d/1oMghClv79tLXwznH7Zgw1BvnMm40N23Djq-XPNMBtpQ/edit)\
[Sprint Backlog](https://github.com/AapoTuulentie/Vuoden-Harmain-Sovellus/blob/main/sprintbacklog.md)\
[Loppuraportti](https://docs.google.com/document/d/1qc828bSGWhAvu27fsx1mrPJhMI1TUBhMevO3DXk0u8E/edit?usp=sharing)

## Projektin asennus
1. Asenna PostgreSQL
2. Asenna poetry
3. Asenna projektin riippuvuudet komennolla ```poetry install```
4. Luo tietokanta psql tulkissa komennolla ```CREATE DATABASE tietokannan_nimi```
5. Tee hakemistoon src tiedosto `.env`, jossa määrittelet PostgreSQL tietokannan osoitteen. Esimerkiksi jos olet luonut tietokannan nimeltä `harmain` voisi env tiedoston ensimmäinen rivi olla: `DATABASE_URL=postgresql:///harmain`
6. Lisää seuraavalle riville myös `SECRET_KEY=sinun_salainen_avain_tähän`
7. Alusta tietokanta ajamalla komento ```psql -d tietokannan_nimi -a -f schema.sql``` projektin juuressa
8. Käynnistä sovellus src hakemistossa komennolla ```flask run```

## Testien ajo
1. Tee tietokanta psql tulkilla, jonka nimi sisältää merkkijonon 'test', esim. `DATABASE_URL=postgresql:///harmaintest`
2. Tee projektin juureen `.env.test` tiedosto, joissa samat tiedot kuin .env tiedostossa, mutta tietokannan osoitteen pitää olla juuri luodun testi-tietokannan nimi.
3. Siirry src hakemistossa virtuaaliympäristöön komennolla ```poetry shell``` ja laita testi-serveri päälle komennolla ```dotenv -f ../.env.test run -- flask run``` 
4. Nyt voit ajaa testit virtuaaliympäristössä ```poetry shell``` komennolla ```robot src/tests``` tai ilman virtuaaliympäristöä komennolla ```poetry run robot src/tests```

## Definition of Done
- Toiminnallisuus on koodattu
- Toiminnallisuudelle on tehty järkevät robot testit, jotka menevät läpi
- Github Actions toimii

![GHA workflow badge](https://github.com/AapoTuulentie/Vuoden-Harmain-Sovellus/workflows/CI/badge.svg)


