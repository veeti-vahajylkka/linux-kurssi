from flask import Flask
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

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
    return f"<h1>Kävijää: {amount_of_visitors}</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)