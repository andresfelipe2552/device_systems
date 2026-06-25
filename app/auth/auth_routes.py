from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.auth import auth_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user
from app.schemas.auth_schema import UserRegister, Token, UserMeResponse
from app.models.user_model import User

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserMeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Crea un nuevo usuario con contraseña segura (hasheada con bcrypt). Límite: 3/min."
)
@limiter.limit("3/minute")
def register(request: Request, data: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data)


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica al usuario y retorna un token JWT Bearer. Límite: 5/min."
)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    from app.schemas.auth_schema import UserLogin
    data = UserLogin(email=form_data.username, password=form_data.password)
    return auth_service.login_user(db, data)


@router.get(
    "/me",
    response_model=UserMeResponse,
    summary="Datos del usuario autenticado",
    description="Retorna los datos del usuario actual usando el token JWT. No expone la contraseña."
)
def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
