from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.database.connection import Base, engine
from app.routes import user_routes, device_routes, loan_routes
from app.auth import auth_routes
from app.middlewares.request_middleware import RequestMiddleware

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title="device_systems API",
    description="""
## API REST segura para gestión de usuarios, dispositivos y préstamos

### Funcionalidades
- **Autenticación** con OAuth2 y tokens JWT
- **Autorización** basada en roles (admin, support, user)
- **Hash seguro** de contraseñas con bcrypt
- **Rate limiting** para prevenir abuso
- **Middleware** de trazabilidad con cabeceras personalizadas
- **CORS** configurado para clientes autorizados

### Roles
| Rol | Permisos |
|-----|----------|
| `admin` | Acceso total |
| `support` | Crear/editar dispositivos, gestionar préstamos |
| `user` | Consultas y préstamos básicos |
    """,
    version="3.0.0",
    contact={"name": "SENA - Ficha 3229209"},
    license_info={"name": "MIT"}
)

# Rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middlewares (orden importa: primero SlowAPI, luego custom, luego CORS)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(RequestMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Device Systems API v3.0 - Segura",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "3.0.0"
    }
