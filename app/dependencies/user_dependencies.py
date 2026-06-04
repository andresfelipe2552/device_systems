from fastapi import Depends, Header, HTTPException, Path, status

# Importamos la DB directamente desde routes para no duplicarla.
# La dependencia recibe la lista por referencia a través del módulo.
from app.routes import user_routes as _routes


# ── 1. Obtener usuario o lanzar 404 ────────────────────────────────────────────
def get_user_or_404(
    user_id: int = Path(..., description="ID del usuario", ge=1)
) -> dict:
    """Busca el usuario por ID en la DB en memoria. Lanza 404 si no existe."""
    user = next((u for u in _routes.users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id={user_id} no encontrado",
        )
    return user


# ── 2. Validar que el correo NO esté en uso ─────────────────────────────────────
def check_email_free(email: str) -> str:
    """Lanza 409 si el correo ya existe en la DB."""
    if any(u["email"] == email for u in _routes.users_db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un usuario con el correo '{email}'",
        )
    return email


# ── 3. Validar rol permitido ─────────────────────────────────────────────────────
ROLES_VALIDOS = {"admin", "support", "user"}

def validate_role(role: str) -> str:
    """Lanza 422 si el rol enviado no está en la lista permitida."""
    if role not in ROLES_VALIDOS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Rol '{role}' no permitido. Válidos: {', '.join(ROLES_VALIDOS)}",
        )
    return role


# ── 4. Autenticación básica por cabecera ─────────────────────────────────────────
API_TOKEN = "device-secret-2025"

def verify_token(
    x_api_token: str = Header(..., description="Token de autenticación: device-secret-2025")
) -> str:
    """Simula autenticación: valida el token en la cabecera X-Api-Token."""
    if x_api_token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o ausente",
        )
    return x_api_token


# ── 5. Configuración general de la API ───────────────────────────────────────────
def get_api_config() -> dict:
    """Retorna metadatos generales de la API, inyectable en cualquier ruta."""
    return {
        "app_name": "device_systems",
        "version": "2.0.0",
        "environment": "development",
    }
