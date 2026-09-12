import sys
import random
from faker import Faker

from src.db import get_connection, init_db

fake = Faker()

GENEROS = ["Estrategia", "Familiar", "Party", "Cartas", "Rol", "Abstracto"]
COMPLEJIDADES = ["baja", "media", "alta"]


def seed(total_juegos=20000, total_editoriales=50):
    init_db()  # asegura que las tablas existan

    conn = get_connection()
    cursor = conn.cursor()

    # Vacia las tablas antes de insertar, para evitar duplicados si se corre 2 veces.
    # Se desactiva la FK temporalmente para poder truncar en orden.
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE TABLE juegos")
    cursor.execute("TRUNCATE TABLE editoriales")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()

    # --- Editoriales ---
    editoriales = [(fake.company()[:150], fake.country()[:100]) for _ in range(total_editoriales)]
    cursor.executemany(
        "INSERT INTO editoriales (nombre, pais) VALUES (%s, %s)", editoriales
    )
    conn.commit()

    cursor.execute("SELECT id FROM editoriales")
    editorial_ids = [row[0] for row in cursor.fetchall()]

    # --- Juegos ---
    sql = """INSERT INTO juegos
             (titulo, genero, complejidad, jugadores_min, jugadores_max, editorial_id)
             VALUES (%s, %s, %s, %s, %s, %s)"""

    lote = []
    insertados = 0
    for _ in range(total_juegos):
        jmin = random.randint(1, 4)
        jmax = jmin + random.randint(0, 4)
        lote.append((
            fake.catch_phrase()[:200],
            random.choice(GENEROS),
            random.choice(COMPLEJIDADES),
            jmin,
            jmax,
            random.choice(editorial_ids),
        ))
        if len(lote) == 1000:
            cursor.executemany(sql, lote)
            conn.commit()
            insertados += len(lote)
            lote = []

    if lote:
        cursor.executemany(sql, lote)
        conn.commit()
        insertados += len(lote)

    cursor.close()
    conn.close()
    print(f"{insertados} juegos insertados correctamente ({total_editoriales} editoriales)")


if __name__ == "__main__":
    total = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    seed(total)
