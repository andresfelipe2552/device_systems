from fastapi import FastAPI
from app.database.connection import create_tables
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**. "
        "Permite crear, listar, consultar, filtrar, actualizar y eliminar usuarios "
        "con persistencia en base de datos mediante **SQLAlchemy**.\n\n"
        "**Cabeceras personalizadas en cada respuesta:**\n"
        "- `X-App-Name: device_systems`\n"
        "- `X-API-Version: 2.0`"
    ),
    version="2.0.0",
    contact={"name": "Equipo device_systems"},
)

# Crear tablas al iniciar la app
create_tables()

app.include_router(user_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app": "device_systems",
        "version": "2.0.0",
        "docs": "/docs",
        "storage": "SQLite via SQLAlchemy",
    }
