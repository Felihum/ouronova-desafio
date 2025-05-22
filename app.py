from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route("/getCoinsData")
def get_coins_data():
    # Captura o parâmetro de query: /getCoinsData?order=desc
    order = request.args.get("order", default="asc").lower()

    # Valida o valor do parâmetro
    if order not in ["asc", "desc"]:
        return jsonify({"error": "Parâmetro 'order' deve ser 'asc' ou 'desc'"}), 400

    # Conecta ao banco
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Executa a query com a ordenação desejada
    cursor.execute(f"""
            SELECT id, timestamp, name, change_24h FROM coins
            ORDER BY timestamp {order.upper()}
        """)
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

    conn.close()
    return jsonify(coins)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
