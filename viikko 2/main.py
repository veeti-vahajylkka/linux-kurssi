from flask import Flask
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#
# Tyylit erotettuna muusta HTML:stä
# Tämä, koska html-templaattimme käyttää F-stringiä {amount_of_visitors}:iin
#       Eli sivuston kävijämäärän näyttämiseen.
#
# CSS tarvitsee aaltosulkeita tyylitysten määrittelyyn, joka ei toimi F-stringissä.
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
                width: 100dvw;
                display: flex;
                justify-content: center;
                font-size: 16px;
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
            }

            h2 {
                margin-bottom: 24px !important;
            }

            p {
                margin-bottom: 12px;
            }

            a {
                display: block;
                width: max-content;
                text-decoration: none;
                padding: 6px 12px;
                border-radius: 6px;
                background-color: #2480c2;
                color: white;
                cursor: pointer;
                margin-bottom: 12px;
                font-size: 18px;
                transition: 0.2s all;
            }

            a:hover {
                transform: translateY(-2px);
                background-color: #1e72ae;
            }
        </style>
    """

def html(amount_of_visitors):
    html_template = f"""
    <html>
        <head>
            <title>Kävijälaskuri</title>

            {styles()}
        </head>

        <body>
            <main class='body-content'>
                <h2>Kävijöitä: {amount_of_visitors}</h2>

                <a
                    href='https://github.com/veeti-vahajylkka/linux-kurssi/tree/main/viikko%202'
                    target='_blank'
                    rel='noreferrer noopener nofollow'
                >
                    Github-repository
                </a>

                <p>
                    Koodissa käytetään <code>environment variable</code> tyyppistä ratkaisua tietokantaan kirjautumiseen.
                </p>

                <p>
                    Sen sijaan että tunnukset olisivat suoraan koodissa (ja versionhallinnassa luettavissa),
                    ovat ne <code>.env</code> tiedostossa piilossa.
                </p>

                <p>
                    Esimerkiksi
                    <code>password = os.getenv('DB_PASSWORD')</code>
                </p>

                <b>Kyseistä tiedostoa ei koskaan julkaista versionhallintaan.</b>

                <h2 style='margin-top: 24px;'>
                    Tietokanta ja taulu
                </h2>

                <p>
                    Loin <code>information</code> nimisen taulun MYSQL-tietokantaan.
                </p>

                <p>
                    Taulussa on <code>kavijat</code> - niminen sarake, tyypiltään
                    
                    <b>
                        INT NOT NULL
                    </b>.
                </p>

                <p>
                    Taulun luontilause:
                    <code>
                        CREATE TABLE information(kavijat INT NOT NULL DEFAULT 0);
                    </code>
                </p>
                
                <h2 style='margin-top: 24px;'>
                    Kävijälaskurin tallennus
                </h2>

                <p>
                    Kävijälaskuri päivittyy SQL-lauseella:

                    <code>
                        UPDATE information SET kavijat = kavijat + 1;
                    </code>
                </p>

                <p>
                    Kävijälaskuri haetaan SQL-lauseella:

                    <code>
                        SELECT kavijat FROM information;
                    </code>
                </p>
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

    cursor.execute("UPDATE information SET kavijat = kavijat + 1;")
    conn.commit()

    cursor.execute("SELECT kavijat FROM information;")
    result = cursor.fetchone()

    amount_of_visitors = result[0]

    # Clean up
    cursor.close()
    conn.close()

    return html(amount_of_visitors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)