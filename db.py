import os
import mysql.connector

conn = mysql.connector.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"],
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS editoriales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    pais VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS juegos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    genero VARCHAR(100),
    complejidad VARCHAR(50),
    jugadores_min INT,
    jugadores_max INT,
    editorial_id INT,
    FOREIGN KEY (editorial_id) REFERENCES editoriales(id)
)
""")

conn.commit()
cursor.close()
conn.close()
print("Tablas creadas correctamente")
