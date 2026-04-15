import os
from flask import Flask, jsonify

app = Flask(__name__)

# Configuración de seguridad básica
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

@app.route("/")
def home():
    # Retorna la respuesta en formato JSON
    return jsonify({
        "status": "success",
        "message": "Hola desde Flask en Docker",
        "pipeline": "AWS CI/CD"
    })

if __name__ == "__main__":
    # Configuración del servidor
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)