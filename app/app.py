import os
from flask import Flask

app = Flask(__name__)

# Seguridad: Clave secreta configurada desde variable de entorno
# En producción, debe establecerse mediante variable de entorno FLASK_SECRET_KEY
# Generar clave segura: python -c "import secrets; print(secrets.token_hex(32))"
# Valor por defecto: 'dev-secret-key-change-in-production' (solo para desarrollo)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

@app.route("/")
def home():
    return "Hola desde Flask en Docker"

if __name__ == "__main__":
    # Seguridad: El modo debug está deshabilitado por defecto
    # Para habilitar: export FLASK_DEBUG=true
    # Valor por defecto: False (seguro para producción)
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)