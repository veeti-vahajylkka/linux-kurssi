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
            }

            .body-content {
                width: 100%;
                max-width: 1200px;
                padding: 2.5rem 0;
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
                <h2>Tervetuloa!</h2>

                <p>
                    Koodissa käytetään <code>environment variable</code> tyyppistä ratkaisua tietokantaan kirjautumiseen,
                    sen sijaan että tunnukset olisivat suoraan koodissa (ja versionhallinnassa luettavissa),
                    ovat ne <code>.env</code> tiedostossa piilossa.

                    <br>

                    <b>Kyseistä tiedostoa ei koskaan julkaista versionhallintaan.</b>
                </p>

                <p>Kävijää: {amount_of_visitors}</p>
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