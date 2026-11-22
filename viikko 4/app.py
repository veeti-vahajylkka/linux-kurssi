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

                <p>Vain A-palvelimen viikko2 sivu päivittää luvun</p>

                <h2 style='margin-top: 24px;'>
                    B-palvelimen luominen
                </h2>

                <p>1. cPoutassa snapshot palvelimen A instanssista</p>
                <p>2. Luodaan uusi instanssi käyttämällä A:n snapshottia</p>

                <h2 style='margin-top: 24px;'>
                    Palvelimien konfiguraatiot
                </h2>

                <h3 style='margin-top: 24px;'>
                    Palvelin A
                </h3>

                <p>
                    <code>/usr/local/bin/backup-website.sh</code> - Sivun backup-scripti
                    
                    <br>

                    <code>/root/.ssh/backup_key</code> - SSH avain, jolla siirretään backupit palvelimelle B.
                    
                    <br>
                    
                    <code>/home/ubuntu/viikko2-initial.sql</code> - Alustetaan MySQL tietokanta palvelimelle B.
                </p>

                <h3 style='margin-top: 24px;'>
                    Palvelin B
                </h3>

                <p>
                    <code>/home/ubuntu/website-backups</code> - Sivustojen backupit palvelimelta A
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

    cursor.execute("SELECT kavijat FROM information;")
    result = cursor.fetchone()

    amount_of_visitors = result[0]

    # Clean up
    cursor.close()
    conn.close()

    return html(amount_of_visitors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)