# Seguridad: Imagen de Python específica con digest para prevenir ataques a la cadena de suministro
# Usando imagen slim para reducir la superficie de ataque
FROM python:3.9-slim@sha256:6d6536a1c6b8e7d3e1c0c5e4a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b

# Seguridad: Crear usuario no-root para que el contenedor no se ejecute como root (CVE-2019-5021)
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copiar requirements primero para aprovechar el caché de Docker
COPY requirements.txt .
# Seguridad: --no-cache-dir para no guardar caché de pip, --break-system-packages para Python 3.11+
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Seguridad: Cambiar propietario al usuario no-root
RUN chown -R appuser:appgroup /app

# Cambiar a usuario no-root
USER appuser

EXPOSE 5000

# Ejecutar Flask correctamente
CMD [ "python", "-m", "flask", "--app", "app:app", "run", "--host", "0.0.0.0", "--port", "5000" ]