# Catálogo de juegos de mesa — Microservicio 1

Microservicio del proyecto **Ludoteca / Red de Cafés de Juegos de Mesa**.
Gestiona el catálogo de juegos de mesa y sus editoriales.

| | |
|---|---|
| **Lenguaje** | Python + Flask |
| **Base de datos** | MySQL |
| **Puerto** | 8001 |
| **Imagen Docker** | `usuario/catalogo-juegos` |

## Tablas

**`editoriales`**

| Columna | Tipo |
|---|---|
| id | INT (PK, auto) |
| nombre | VARCHAR(150) |
| pais | VARCHAR(100) |

**`juegos`**

| Columna | Tipo |
|---|---|
| id | INT (PK, auto) |
| titulo | VARCHAR(200) |
| genero | VARCHAR(100) |
| complejidad | VARCHAR(50) |
| jugadores_min | INT |
| jugadores_max | INT |
| editorial_id | INT (FK → editoriales.id) |

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/juegos` | Listar todos los juegos |
| GET | `/juegos/{id}` | Obtener un juego |
| POST | `/juegos` | Crear un juego |
| PUT | `/juegos/{id}` | Actualizar un juego |
| DELETE | `/juegos/{id}` | Eliminar un juego |
| GET | `/editoriales` | Listar editoriales |
| GET | `/editoriales/{id}` | Obtener una editorial |

Documentación interactiva (Swagger UI): **`/api-docs/`**
Spec OpenAPI en JSON crudo: **`/api-docs.json`**

## Variables de entorno

Copia `.env.example` a `.env` y completa los valores:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=catalogo
PORT=8001
```

> Nunca se hardcodea `localhost` dentro del código — todo se lee de variables de entorno (`src/db.py`). En despliegue, `DB_HOST` apunta a la VM/servicio real de MySQL.

## Cómo correr en local (sin Docker)

```bash
pip install -r requirements.txt
cp .env.example .env   # y completa tus valores
# exporta las variables o usa python-dotenv
python server.py
```

El servidor queda escuchando en `http://localhost:8001`.

## Cómo correr con Docker

```bash
docker build -t usuario/catalogo-juegos .

docker run -d --name catalogo-juegos \
  -p 8001:8001 \
  -e DB_HOST=host.docker.internal \
  -e DB_USER=root \
  -e DB_PASSWORD=root \
  -e DB_NAME=catalogo \
  usuario/catalogo-juegos
```

En el `docker-compose` final del proyecto, `DB_HOST` apuntará al nombre del servicio de MySQL dentro de la red de contenedores (ej. `mysql-catalogo`).

## Datos de prueba (carga masiva)

Se incluye un script de seed que inserta **20,000 juegos ficticios** (más 50 editoriales) generados con [`Faker`](https://faker.readthedocs.io/).

```bash
python -m src.seed              # inserta 20,000 juegos (default)
python -m src.seed 30000        # inserta una cantidad distinta
```

> ⚠️ El script vacía las tablas `juegos` y `editoriales` antes de insertar, para evitar duplicados si se corre más de una vez. Está pensado para ejecutarse una sola vez, de forma manual (no se dispara al iniciar el servidor).

## Pruebas

Se incluye una colección de Postman (`catalogo-juegos-postman-collection.json`) con el CRUD completo, casos de éxito y casos de error (recurso inexistente → 404, body inválido → 400), con asserts automáticos.

Para correrla:
1. Importa el archivo en Postman.
2. Ajusta la variable de colección `base_url` si tu servicio no corre en `http://localhost:8001`.
3. Click derecho en la colección → **Run collection**.

## Estructura del proyecto

```
catalogo-juegos/
├── src/
│   ├── app.py                    # configuración de Flask, CORS, blueprints y Swagger
│   ├── db.py                     # conexión a MySQL vía variables de entorno + creación de tablas
│   ├── swagger.py                # configuración de flasgger / OpenAPI
│   ├── seed.py                   # script de carga masiva de datos ficticios
│   └── routes/
│       ├── juegos_routes.py      # endpoints de juegos documentados con Swagger
│       └── editoriales_routes.py # endpoints de editoriales
├── server.py                     # punto de entrada, levanta el servidor en el puerto 8001
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── .env.example
```
