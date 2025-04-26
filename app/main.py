from flask import Flask, request, jsonify
from processor import procesar_logs

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_event():
    print("🛰️ Evento recibido, comenzando procesamiento...")
    resultado = procesar_logs()
    return jsonify(resultado), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

