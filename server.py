import os
from src.app import create_app
from src.db import init_db

app = create_app()

if __name__ == "__main__":
    init_db()  # crea las tablas si no existen
    port = int(os.environ.get("PORT", 8001))
    app.run(host="0.0.0.0", port=port)
