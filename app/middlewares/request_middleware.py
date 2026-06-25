import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("device_systems")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


class RequestMiddleware(BaseHTTPMiddleware):
    """
    Middleware personalizado que:
    - Mide el tiempo de respuesta
    - Agrega cabeceras X-Process-Time, X-App-Name y X-Request-ID
    - Registra método, ruta y código de estado de cada petición
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Generar o propagar X-Request-ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])

        response = await call_next(request)

        process_time = round(time.time() - start_time, 4)

        # Agregar cabeceras personalizadas
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id

        # Registrar la petición
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} -> "
            f"{response.status_code} ({process_time}s)"
        )

        return response
