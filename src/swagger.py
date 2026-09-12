swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/api-docs.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api-docs/",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Catalogo de juegos de mesa - Microservicio 1",
        "description": "CRUD de juegos y editoriales (Ludoteca / Red de Cafes de Juegos de Mesa).",
        "version": "1.0.0",
    },
    "tags": [
        {"name": "juegos", "description": "Operaciones sobre juegos"},
        {"name": "editoriales", "description": "Operaciones sobre editoriales"},
    ],
}
