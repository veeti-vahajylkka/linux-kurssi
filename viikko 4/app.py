
from flask import Flask
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


#
# Tyylit erotettuna muusta HTML:stä
# Tämä, koska html-templaattimme käyttää F-stringiä {amount_of_visitors}:iin
# CSS tarvitsee aaltosulkeita tyylitysten määrittelyyn.
#
def styles():
    return """
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: sans-serif;
                display: flex;
                justify-content: center;
                font-size: 16px;
                line-height: 1.6;
                padding-bottom: 2.5rem;
            }

            .body-content {
                width: 90%;
                max-width: 1200px;
                padding: 2.5rem 0;
            }

            code {
                padding: 2px 4px;
                background: #f4f4f4;
                border: 1px solid #d3d3d3;
                border-radius: 6px;
                font-weight: 600;
                overflow-wrap: anywhere;
            }

            h2 {
                margin-bottom: 24px !important;
            }

            h3 {
                margin-top: 24px;
                margin-bottom: 12px;
            }

            p {
                margin-bottom: 12px;
            }

            ul, ol {
                margin: 0 0 20px 24px;
            }

            li {
                margin-bottom: 8px;
            }

            .info-box {
                padding: 16px;
                border: 1px solid #d3d3d3;
                border-radius: 8px;
                margin-bottom: 20px;
                background: #fafafa;
            }

            .server-label {
                color: #2480c2;
                font-weight: bold;
            }

            .section {
                margin-top: 36px;
            }

            .comparison {
                width: 100%;
                border-collapse: collapse;
                margin: 16px 0 24px;
            }

            .comparison th,
            .comparison td {
                border: 1px solid #d3d3d3;
                padding: 10px;
                text-align: left;
                vertical-align: top;
            }

            .comparison th {
                background: #f4f4f4;
            }
        </style>
    """


def html(amount_of_visitors):
    html_template = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Kävijälaskuri - Server B</title>
            {styles()}
        </head>

        <body>
            <main class='body-content'>

                <h2>Kävijöitä: {amount_of_visitors}</h2>

                <p><b>Server B - Vain luku - kopio</b></p>
                <p>Tämän sivun uudelleenlataaminen ei päivitä kävijämäärää.</p>

                <a
                    href='http://195.148.20.90/viikko2/'
                    target='_blank'
                    rel='noreferrer noopener nofollow'
                >
                    Viikko 2 - Server A
                </a>

                <br>

                <a
                    href='https://github.com/veeti-vahajylkka/linux-kurssi/tree/main/viikko%204'
                    target='_blank'
                    rel='noreferrer noopener nofollow'
                >
                    Github-repositorio
                </a>

                <p>Vain A-palvelimen viikko2-sivu päivittää kävijämäärää.</p>


                <div class="section">
                    <h2>Palvelimen B luominen</h2>

                    <ol>
                        <li>Otetaan cPoutassa snapshot palvelimen A instanssista.</li>
                        <li>Luodaan uusi instanssi käyttämällä A:n snapshotia.</li>
                        <li>Konfiguroidaan palvelimen B verkko- ja tietokantayhteydet.</li>
                        <li>Otetaan käyttöön MySQL-replikointi palvelimien välillä.</li>
                        <li>Konfiguroidaan automaattiset verkkosivujen varmuuskopiot.</li>
                    </ol>
                </div>


                <div class="section">
                    <h2>Palvelimien konfiguraatiot</h2>

                    <h3>Palvelin A - Primary</h3>
                    <p class="server-label">IP-osoite: 195.148.20.90</p>

                    <div class="info-box">
                        <p>
                            <code>/var/www/html</code>
                            - Varmuuskopioitavat verkkosivut.
                        </p>

                        <p>
                            <code>/usr/local/bin/backup-website.sh</code>
                            - Sivuston varmuuskopiointiskripti.
                        </p>

                        <p>
                            <code>/root/.ssh/backup_key</code>
                            - SSH-yksityisavain, jolla siirretään varmuuskopiot palvelimelle B.
                        </p>

                        <p>
                            <code>/var/log/website-backup.log</code>
                            - Varmuuskopiointiskriptin lokitiedosto.
                        </p>

                        <p>
                            <code>/home/ubuntu/viikko2-initial.sql</code>
                            - Alkuperäinen MySQL-tietokannan vientitiedosto, jota käytettiin B-palvelimen alustamiseen.
                        </p>
                    </div>


                    <h3>Palvelin B - Replica</h3>
                    <p class="server-label">IP-osoite: 195.148.23.192</p>

                    <div class="info-box">
                        <p>
                            <code>/home/ubuntu/website-backups</code>
                            - Palvelimelta A vastaanotetut verkkosivujen varmuuskopiot.
                        </p>

                        <p>
                            <code>/home/ubuntu/lemp-app</code>
                            - Palvelimen B Flask-sovellus.
                        </p>

                        <p>
                            <code>/etc/mysql/mysql.conf.d/replication.cnf</code>
                            - MySQL-replikoinnin konfiguraatio.
                        </p>

                        <p>
                            <code>/var/lib/mysql</code>
                            - Paikallisesti tallennettu MySQL-tietokanta.
                        </p>
                    </div>
                </div>


                <div class="section">
                    <h2>Tuntikohtaiset verkkosivujen varmuuskopiot</h2>

                    <p>
                        Palvelin A suorittaa automaattisen verkkosivujen
                        varmuuskopioinnin joka tunti cron-ajastuksen avulla.
                    </p>

                    <div class="info-box">
                        <p><b>Cron-konfiguraatio:</b></p>
                        <code>0 * * * * /usr/local/bin/backup-website.sh</code>

                        <p style="margin-top: 12px;">
                            Tämä tarkoittaa, että skripti suoritetaan jokaisen
                            tunnin alussa, esimerkiksi klo 08:00, 09:00 ja 10:00.
                        </p>
                    </div>

                    <h3>Varmuuskopioinnin toimintaperiaate</h3>

                    <ol>
                        <li>
                            Palvelin A lukee verkkosivujen tiedostot
                            hakemistosta <code>/var/www/html</code>.
                        </li>
                        <li>
                            Tiedostot siirretään palvelimelle B
                            <code>rsync</code>-komennolla SSH-yhteyden kautta.
                        </li>
                        <li>
                            Varmuuskopiot tallennetaan palvelimelle B
                            hakemistoon <code>/home/ubuntu/website-backups</code>.
                        </li>
                        <li>
                            Skripti säilyttää kaksi viimeisintä onnistunutta
                            varmuuskopiota.
                        </li>
                    </ol>

                    <p>
                        Skriptin suorituslokit tallennetaan palvelimella A
                        tiedostoon <code>/var/log/website-backup.log</code>.
                    </p>
                </div>


                <div class="section">
                    <h2>Jatkuva MySQL-replikointi</h2>

                    <p>
                        Palvelimien välillä on jatkuva MySQL-replikointi.
                        Palvelin A toimii ensisijaisena tietokantapalvelimena
                        ja palvelin B toimii sen replika-palvelimena.
                    </p>

                    <h3>Replikoinnin toimintaperiaate</h3>

                    <ol>
                        <li>
                            Palvelimella A tapahtuvat tietokantamuutokset
                            tallentuvat MySQL:n binäärilokeihin (binary logs).
                        </li>
                        <li>
                            Palvelin B lukee muutokset palvelimelta A
                            jatkuvasti replikointiyhteyden kautta.
                        </li>
                        <li>
                            Palvelin B soveltaa vastaanotetut muutokset
                            omaan paikalliseen tietokantaansa.
                        </li>
                        <li>
                            Tietokannan sisältö pysyy näin synkronoituna
                            palvelimien välillä.
                        </li>
                    </ol>

                    <div class="info-box">
                        <p><b>Replikoinnin asetukset:</b></p>
                        <ul>
                            <li>Ensisijainen palvelin: A (195.148.20.90)</li>
                            <li>Replika-palvelin: B (195.148.23.192)</li>
                            <li>Tietokanta: <code>viikko2</code></li>
                            <li>Yhteys: SSL-salattu MySQL-yhteys</li>
                            <li>Replikointi: MySQL binary log -pohjainen replikointi</li>
                        </ul>
                    </div>

                    <h3>Palvelimen B vain luku -tila</h3>

                    <p>
                        Palvelimella B on käytössä asetukset
                        <code>read_only=ON</code> ja
                        <code>super_read_only=ON</code>.
                    </p>

                    <p>
                        Näiden asetusten avulla estetään normaalit
                        tietokantamuutokset palvelimella B. Flask-sovellus
                        lukee kävijämäärän paikallisesta tietokannasta
                        SELECT-kyselyllä, mutta ei muuta sitä.
                    </p>

                    <p>
                        Kävijämäärän päivittäminen tapahtuu ainoastaan
                        palvelimen A sovelluksessa.
                    </p>
                </div>


                <div class="section">
                    <h2>Varmuuskopioinnin ja replikoinnin erot</h2>

                    <p>
                        Varmuuskopiointi ja tietokannan replikointi ovat
                        kaksi erillistä toimintoa, joilla on eri tarkoitukset.
                    </p>

                    <table class="comparison">
                        <thead>
                            <tr>
                                <th>Ominaisuus</th>
                                <th>Varmuuskopiointi</th>
                                <th>Replikointi</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr>
                                <td>Suoritustiheys</td>
                                <td>Joka tunti</td>
                                <td>Jatkuvasti</td>
                            </tr>
                            <tr>
                                <td>Suunta</td>
                                <td>A → B</td>
                                <td>A → B</td>
                            </tr>
                            <tr>
                                <td>Menetelmä</td>
                                <td>rsync ja SSH</td>
                                <td>MySQL binary logs</td>
                            </tr>
                            <tr>
                                <td>Data</td>
                                <td>Verkkosivujen tiedostot</td>
                                <td>Tietokantamuutokset</td>
                            </tr>
                            <tr>
                                <td>Tarkoitus</td>
                                <td>Tiedostojen palauttaminen</td>
                                <td>Tietokannan synkronointi</td>
                            </tr>
                            <tr>
                                <td>Säilytys</td>
                                <td>Kaksi viimeisintä onnistunutta kopiota</td>
                                <td>Ei erillistä historiallista varmuuskopiointia</td>
                            </tr>
                        </tbody>
                    </table>
                </div>


                <div class="section">
                    <h2>Replikointi ei korvaa varmuuskopiointia</h2>

                    <p>
                        Jatkuva replikointi pitää palvelimen B tietokannan
                        ajan tasalla, mutta se ei itsessään tarjoa
                        historiallisia tietokantavarmuuskopioita.
                    </p>

                    <p>
                        Esimerkiksi jos tietokannasta poistetaan vahingossa
                        tietoja palvelimella A, myös poistot voivat
                        replikoitua palvelimelle B.
                    </p>

                    <p>
                        Tämän vuoksi tietokannasta tulisi ottaa myös
                        erillisiä varmuuskopioita, jotta tietoja voidaan
                        palauttaa aikaisempaan tilaan.
                    </p>
                </div>

                <div class="section">
                    <h2>Linux-käyttäjät, tietokantakäyttäjät ja käyttöoikeudet</h2>

                    <h3>Linux-käyttäjät</h3>

                    <div class="info-box">
                        <p>
                            <b>ubuntu</b> - Tavallinen ylläpitokäyttäjä, jolla hallitaan
                            palvelimia SSH-yhteyden kautta. Palvelimen B Flask-sovellus
                            sijaitsee tämän käyttäjän kotihakemistossa.
                        </p>

                        <p>
                            <b>root</b> - Järjestelmän pääkäyttäjä. Varmuuskopiointiskripti
                            suoritetaan root-käyttäjän cron-ajastuksella. Myös SSH-yksityisavain
                            sijaitsee root-käyttäjän suojatussa hakemistossa.
                        </p>

                        <p>
                            <b>www-data</b> - Verkkopalveluiden käyttämä ryhmä.
                            Gunicorn suorittaa Flask-sovellusta käyttäjänä ubuntu
                            ja ryhmällä www-data.
                        </p>
                    </div>

                    <h3>MySQL-käyttäjät</h3>

                    <div class="info-box">
                        <p>
                            <b>repl</b> - Palvelimen A MySQL-käyttäjä, jolla on
                            REPLICATION SLAVE -oikeus. Käyttäjää käytetään palvelimen B
                            replikointiyhteydessä.
                        </p>

                        <p>
                            <b>viikko4_reader</b> - Palvelimen B Flask-sovelluksen
                            tietokantakäyttäjä. Käyttäjällä on ainoastaan SELECT-oikeus
                            tietokantaan viikko2.
                        </p>
                    </div>

                    <h3>Tiedostojen omistajuus ja oikeudet</h3>

                    <ul>
                        <li>
                            Varmuuskopiointiskriptin käyttöoikeus on 700,
                            joten vain root-käyttäjä voi lukea, muokata ja suorittaa sen.
                        </li>
                        <li>
                            Flask-sovelluksen hakemisto kuuluu ubuntu-käyttäjälle.
                        </li>
                        <li>
                            Flask-sovelluksen .env-tiedoston oikeudet ovat 600,
                            joten vain tiedoston omistaja voi lukea ja muokata sitä.
                        </li>
                        <li>
                            SSH-yksityisavain sijaitsee root-käyttäjän suojatussa
                            SSH-hakemistossa.
                        </li>
                        <li>
                            MySQL:n read_only- ja super_read_only-asetukset estävät
                            normaalit tietokantakirjoitukset palvelimella B.
                        </li>
                    </ul>
                </div>


                <div class="section">
                    <h2>Testitulokset</h2>

                    <h3>MySQL-replikoinnin tila</h3>

                    <p>
                        Replikoinnin tila tarkistettiin palvelimella B komennolla
                        <code>SHOW REPLICA STATUS\G</code>.
                    </p>

                    <div class="info-box">
                        <p><b>Testitulokset:</b></p>
                        <ul>
                            <li>Replica_IO_Running: Yes</li>
                            <li>Replica_SQL_Running: Yes</li>
                            <li>Seconds_Behind_Source: 0</li>
                            <li>Replikoinnin virhekentät olivat tyhjiä.</li>
                        </ul>
                    </div>

                    <h3>Kävijämäärän synkronointi</h3>

                    <p>
                        Replikointi testattiin kasvattamalla kävijämäärää palvelimella A.
                        Tämän jälkeen palvelimen B tietokannasta tarkistettiin sama arvo.
                    </p>

                    <div class="info-box">
                        <p><b>Testin tulos:</b></p>
                        <ul>
                            <li>Palvelimen A kävijämäärä: 36</li>
                            <li>Palvelimen B kävijämäärä: 36</li>
                        </ul>
                        <p>
                            Testi osoitti, että tietokantamuutokset replikoituivat
                            onnistuneesti palvelimelta A palvelimelle B.
                        </p>
                    </div>

                    <h3>Vain luku -tilan tarkistus</h3>

                    <p>
                        Palvelimella B tarkistettiin MySQL-asetukset:
                    </p>

                    <ul>
                        <li>read_only = 1</li>
                        <li>super_read_only = 1</li>
                    </ul>

                    <h3>Flask-sovelluksen testaus</h3>

                    <p>
                        Flask-sovellus testattiin paikallisesti palvelimella B
                        komennolla <code>curl -i http://127.0.0.1:5001/</code>.
                        Sovellus palautti onnistuneesti HTML-sivun ja tietokannasta
                        luetun kävijämäärän.
                    </p>
                </div>


                <div class="section">
                    <h2>Ratkaistu ongelma ja opitut asiat</h2>

                    <p>
                        Yksi työn aikana ratkaistu ongelma liittyi palvelimen B
                        Flask-sovellukseen. Sovellus yritti aluksi kasvattaa
                        kävijämäärää SQL-komennolla:
                    </p>

                    <p>
                        <code>UPDATE information SET kavijat = kavijat + 1;</code>
                    </p>

                    <p>
                        Tämä aiheutti virheen, koska palvelimen B MySQL-tietokanta
                        oli määritetty vain luku -tilaan.
                    </p>

                    <p>
                        Ongelma ratkaistiin muuttamalla palvelimen B sovellus
                        suorittamaan ainoastaan SELECT-kysely kävijämäärän lukemiseksi.
                        Tämän jälkeen sovellus pystyi näyttämään palvelimen A
                        päivittämän kävijämäärän ilman tietokannan muokkaamista.
                    </p>

                    <p>
                        Työn aikana opin erityisesti MySQL-replikoinnin toimintaperiaatteen,
                        Linuxin cron-ajastuksen käytön sekä SSH-avaimilla toteutettavan
                        palvelimien välisen tiedostonsiirron.
                    </p>

                    <p>
                        Opin myös, että tietokannan replikointi ei korvaa erillistä
                        varmuuskopiointia, koska myös virheelliset muutokset voivat
                        replikoitua toiselle palvelimelle.
                    </p>
                </div>
            </main>
        </body>
    </html>
    """

    return html_template


@app.route('/')
def home():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_DATABASE')
    )

    cursor = conn.cursor()

    cursor.execute("SELECT kavijat FROM information;")
    result = cursor.fetchone()

    amount_of_visitors = result[0]

    # Clean up
    cursor.close()
    conn.close()

    return html(amount_of_visitors)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)