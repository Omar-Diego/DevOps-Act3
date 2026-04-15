# DevOps-Act3

## Descripción del Proyecto

Este proyecto es una aplicación web básica desarrollada con **Flask** (Python) y containerizada utilizando **Docker**. El objetivo es demostrar los conceptos fundamentales de DevOps mediante la contenedorización de una aplicación simple.

## Estructura del Proyecto

```
DevOps-Act3/
├── README.md
└── app/
    ├── app.py          # Aplicación principal de Flask
    ├── Dockerfile      # Configuración para construir la imagen Docker
    ├── docker-compose.yml    # Configuración de servicios Docker
    └── requirements.txt      # Dependencias de Python
```

## Requisitos Previos

- Python 3.9 o superior
- Docker
- Docker Compose

## Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd DevOps-Act3
```

### 2. Construir y Ejecutar con Docker Compose

La forma más sencilla de ejecutar la aplicación es utilizando Docker Compose:

```bash
cd app
docker-compose up --build
```

Esto construirá la imagen Docker y levantará el contenedor. La aplicación estará disponible en `http://localhost:5000`.

### 3. Ejecutar la Aplicación Directamente (Sin Docker)

Si prefieres ejecutar la aplicación sin containerización:

```bash
cd app
pip install -r requirements.txt
python app.py
```

La aplicación se iniciara en `http://localhost:5000`.

## Componentes del Proyecto

### Aplicación Flask (`app.py`)

Una aplicación web simple que devuelve el mensaje "Hola desde Flask en Docker" en la ruta principal (`/`).

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hola desde Flask en Docker"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### Dockerfile

Define la imagen Docker basada en Python 3.9:

- Establece el directorio de trabajo en `/app`
- Copia el archivo de dependencias
- Instala las dependencias de Python
- Expone el puerto 5000
- Ejecuta la aplicación Flask

### Docker Compose

Configura un servicio web que:

- Construye la imagen desde el directorio `./app`
- Mapea el puerto 5000 del contenedor al puerto 5000 del host

### Dependencies (`requirements.txt`)

Contiene una única dependencia: Flask, el framework web utilizado.

## Comandos Útiles

### Iniciar la aplicación

```bash
docker-compose up
```

### Iniciar en modo detach (segundo plano)

```bash
docker-compose up -d
```

### Ver logs del contenedor

```bash
docker-compose logs -f
```

### Detener los contenedores

```bash
docker-compose down
```

### Reconstruir la imagen

```bash
docker-compose build --no-cache
```

## Verificación

Para verificar que la aplicación está funcionando correctamente:

1. Inicia los contenedores con `docker-compose up -d`
2. Abre tu navegador y visita `http://localhost:5000`
3. Deberías ver el mensaje: "Hola desde Flask en Docker"

También puedes usar `curl` para verificar:

```bash
curl http://localhost:5000
```

## Tecnologías Utilizadas

- **Python 3.9**: Lenguaje de programación
- **Flask**: Framework web de Python
- **Docker**: Plataforma de containerización
- **Docker Compose**: Herramienta para definir y ejecutar aplicaciones multi-contenedor
