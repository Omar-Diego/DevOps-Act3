FROM python:3.9-slim

# Seguridad: Crear usuario y grupo no-root
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Copiar requirements primero para aprovechar caché
COPY requirements.txt .

# Quitar la bandera break-system-packages porque en Python 3.9 no existe
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Cambiar de propietario los archivos ubicados en la ruta de trabajo
RUN chown -R appuser:appgroup /app

# Ahora sí, usar ese usuario no privilegiado para ejecutar
USER appuser

EXPOSE 5000

# Usar python original de tu archivo app.py
CMD [ "python", "app.py" ]