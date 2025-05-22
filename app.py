from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/getCoinsData")
def get_coins_data():
    # Conecta ao banco
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Busca todos os registros
    cursor.execute("SELECT id, timestamp, name, change_24h FROM coins")
    rows = cursor.fetchall()

    # Converte os dados para dicionários
    coins = []
    for row in rows:
        coins.append({
            "id": row[0],
            "timestamp": row[1],
            "name": row[2],
            "change_24h": row[3]
        })

    # Fecha a conexão
    conn.close()

    # Retorna como JSON
    return jsonify(coins)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
