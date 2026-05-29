from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**. "
        "Permite listar, consultar, filtrar y registrar usuarios con validaciones Pydantic."
    ),
    version="1.0.0",
    contact={"name": "Equipo device_systems"},
)

app.include_router(user_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app": "device_systems",
        "version": "1.0.0",
        "docs": "/docs",
    }
