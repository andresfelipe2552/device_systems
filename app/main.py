from fastapi import FastAPI, Request
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**.\n\n"
        "Permite listar, consultar, filtrar, crear, actualizar y eliminar usuarios "
        "con validaciones Pydantic, manejo de errores HTTP y Dependency Injection."
    ),
    version="2.0.0",
    contact={"name": "Equipo device_systems", "email": "soporte@device.com"},
    license_info={"name": "MIT"},
    openapi_tags=[
        {
            "name": "Usuarios",
            "description": "Operaciones CRUD completas sobre el recurso **usuarios**.",
        }
    ],
)

# ── Middleware: cabeceras personalizadas en todas las respuestas ────────────────
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0.0"
    return response


app.include_router(user_router)


@app.get("/", tags=["Root"], summary="Bienvenida")
def root():
    return {
        "app": "device_systems",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }
