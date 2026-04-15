# DevOps-Act3 - Aplicación Flask con Mejoras de Seguridad

## Descripción del Proyecto

Este proyecto es una aplicación web desarrollada con **Flask** (Python) y containerizada con **Docker**. La aplicación está diseñada siguiendo las mejores prácticas de seguridad para entornos de producción, incluyendo configuración de variables de entorno, usuario no-root, límites de recursos y versiones dependientes aseguradas.

## Características de Seguridad Implementadas

### 1. Seguridad en la Aplicación Flask (`app.py`)

- **Clave secreta configurable**: La variable de entorno `FLASK_SECRET_KEY` permite establecer una clave segura para las sesiones de Flask. Valor por defecto: `dev-secret-key-change-in-production` (solo para desarrollo).
- **Modo debug controlado**: La variable de entorno `FLASK_DEBUG` controla el modo de depuración. Valor por defecto: `false` (seguro para producción).

### 2. Seguridad en el Dockerfile

- **Usuario no-root**: Se crea un usuario y grupo especiales (`appuser`/`appgroup` con UID/GID 1000) para ejecutar la aplicación sin privilegios de administrador.
- **Versión de Python fijada**: Se utiliza `python:3.9-slim` para garantizar consistencia y facilitar actualizaciones de seguridad.
- **Permisos adecuados**: Los archivos del proyecto son propiedad del usuario no-root.

### 3. Seguridad en Docker Compose

- **Sistema de archivos de solo lectura** (`read_only: true`): Previene modificaciones no autorizadas al sistema de archivos del contenedor.
- **Sin privilegios nuevos** (`no-new-privileges: true`): Impide que el contenedor adquiera privilegios adicionales.
- **Límites de recursos**:
  - CPU: máximo 0.5 núcleos, reserva 0.25 núcleos
  - Memoria: máximo 256MB, reserva 128MB
- **Healthcheck configurado**: Verifica la salud del contenedor cada 30 segundos.
- **Variables de entorno seguras**: `FLASK_DEBUG=false` y `FLASK_ENV=production` configurados por defecto.

### 4. Seguridad en Dependencias (`requirements.txt`)

- **Versiones de Flask fijadas**: `>=2.3.0,<3.1.0` para recibir parches de seguridad sin cambios rompeedores.
- **Werkzeug explícito**: Versión `>=2.3.0,<3.1.0` que incluye correcciones de seguridad para vulnerabilidades como request smuggling.

### 5. Seguridad en AWS CodeBuild (`buildspec.yml`)

- **Autenticación segura en ECR**: Uso de `get-login-password` sin almacenar contraseñas en logs.
- **Build args para trazabilidad**: Información de fecha de construcción y referencia VCS embebida en la imagen.
- **Validación de salida JSON**: Validación antes de generar `imagedefinitions.json`.
- **Registro de digest de imagen**: Trazabilidad completa de la imagen construida.
- **Comentarios de configuración segura**: Documentación para usar SSM Parameter Store en producción.

## Variables de Entorno

**No se necesita archivo `.env`** - Los valores por defecto están configurados para permitir ejecución inmediata.

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `FLASK_SECRET_KEY` | `dev-secret-key-change-in-production` | Clave secreta para sesiones Flask. **En producción debe establecerse un valor seguro.** |
| `FLASK_DEBUG` | `false` | Habilita el modo debug de Flask. En producción debe remain `false`. |
| `FLASK_ENV` | `production` | Entorno de ejecución de Flask. |

**Para generar una clave segura en producción:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Estructura del Proyecto

```
DevOps-Act3/
├── README.md                 # Este archivo
├── buildspec.yml             # Configuración de AWS CodeBuild
└── app/
    ├── app.py                # Aplicación Flask con seguridad
    ├── Dockerfile            # Imagen Docker con usuario no-root
    ├── docker-compose.yml    # Configuración con límites de seguridad
    └── requirements.txt      # Dependencias con versiones seguras
```

## Requisitos Previos

- Python 3.9 o superior
- Docker
- Docker Compose

## Instalación y Configuración

### Opción 1: Docker Compose (Recomendado)

```bash
cd app
docker-compose up --build
```

La aplicación estará disponible en `http://localhost:5000`.

### Opición 2: Ejecución Local (Desarrollo)

```bash
cd app
pip install -r requirements.txt
python app.py
```

La aplicación estará disponible en `http://localhost:5000`.

## Comandos para Ejecutar la Aplicación

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

### Verificar estado del contenedor

```bash
docker-compose ps
```

## Verificación

Para verificar que la aplicación está funcionando correctamente:

1. Inicia los contenedores: `docker-compose up -d`
2. Verifica el healthcheck: `docker-compose ps` (debe mostrar "healthy")
3. Accede a la aplicación: `http://localhost:5000`
4. Deberías ver el mensaje: "Hola desde Flask en Docker"

También puedes usar `curl`:

```bash
curl http://localhost:5000
```

Para verificar las variables de entorno del contenedor:

```bash
docker-compose exec web env
```

## Recomendaciones de Seguridad para Producción

### 1. Variables de Entorno

- Establecer `FLASK_SECRET_KEY` con un valor seguro generado aleatoriamente.
- Mantener `FLASK_DEBUG=false` y `FLASK_ENV=production`.
- No usar valores por defecto en entornos de producción.

### 2. Docker

- Mantener `read_only: true` para prevenir modificaciones al sistema de archivos.
- Usar `--no-new-privileges: true` para evitar escalada de privilegios.
- Establecer límites de memoria apropiados para la aplicación.
- Implementar logs de auditoría.

### 3. Red

- Usar un reverse proxy (nginx, Traefik) para terminación SSL/TLS.
- Configurar firewall para permitir solo puertos necesarios.
- Considerar el uso de redes aisladas entre contenedores.

### 4. Imágenes Docker

- Usar imágenes oficiales de Python con versiones LTS.
- Escanear imágenes regularmente con herramientas como Trivy o Clair.
- Actualizar dependencias regularmente para obtener parches de seguridad.
- Eliminar herramientas de desarrollo de las imágenes de producción.

### 5. AWS CodeBuild

- Almacenar credenciales de ECR en AWS Secrets Manager o SSM Parameter Store.
- Implementar análisis de vulnerabilidades en el pipeline CI/CD.
- Usar IAM roles en lugar de claves de acceso.
- Habilitar cifrado en reposo para artefactos.

### 6. Monitoreo

- Implementar alertas para uso de recursos anómalo.
- Configurar logging centralizado.
- Usar herramientas como AWS CloudWatch o Prometheus+Grafana.

## Tecnologías Utilizadas

- **Python 3.9**: Lenguaje de programación
- **Flask 2.3.x**: Framework web de Python
- **Werkzeug 2.3.x**: Biblioteca WSGI con parches de seguridad
- **Docker**: Plataforma de containerización
- **Docker Compose**: Herramienta para definir y ejecutar aplicaciones multi-contenedor
- **AWS CodeBuild**: Servicio de construcción en la nube
- **Amazon ECR**: Registro de contenedores de AWS
