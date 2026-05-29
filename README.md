# device_systems API

API REST para la **gestión de usuarios** del sistema `device_systems`, construida con **FastAPI** y validaciones **Pydantic v2**.

---

## Descripción

`device_systems` expone un conjunto de endpoints para administrar usuarios internos. Cada usuario tiene nombre, correo electrónico, rol y estado activo. La API aplica validaciones automáticas, evita registros duplicados y retorna cabeceras HTTP personalizadas en cada respuesta.

---

## Instalación de dependencias

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/device_systems.git
cd device_systems

# Crear entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt
```

> Si usas **uv**: `uv sync`

---

## Ejecución del servidor

```bash
uvicorn app.main:app --reload
```

El servidor quedará disponible en: `http://127.0.0.1:8000`

---

## Tabla de endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/users` | Lista todos los usuarios |
| `GET` | `/users?role=admin` | Filtra por rol (`admin`, `support`, `user`) |
| `GET` | `/users?is_active=true` | Filtra por estado activo/inactivo |
| `GET` | `/users/{user_id}` | Obtiene un usuario por ID (path parameter) |
| `POST` | `/users` | Registra un nuevo usuario |

---

## Ejemplos de peticiones

### GET /users — listar todos los usuarios

```http
GET http://127.0.0.1:8000/users
```

**Respuesta 200:**
```json
[
  { "id": 1, "name": "Carlos Ruiz", "email": "carlos.ruiz@device.com", "role": "admin", "is_active": true },
  { "id": 2, "name": "María López", "email": "maria.lopez@device.com", "role": "support", "is_active": true }
]
```

---

### GET /users?role=admin — filtrar por rol

```http
GET http://127.0.0.1:8000/users?role=admin
```

---

### GET /users?is_active=false — filtrar por estado

```http
GET http://127.0.0.1:8000/users?is_active=false
```

---

### GET /users/{user_id} — obtener por ID

```http
GET http://127.0.0.1:8000/users/1
```

**Respuesta 200:**
```json
{ "id": 1, "name": "Carlos Ruiz", "email": "carlos.ruiz@device.com", "role": "admin", "is_active": true }
```

**Respuesta 404 (ID inexistente):**
```json
{ "detail": "Usuario con id=99 no encontrado" }
```

---

### POST /users — crear usuario

```http
POST http://127.0.0.1:8000/users
Content-Type: application/json

{
  "name": "Laura Gómez",
  "email": "laura.gomez@device.com",
  "role": "support",
  "is_active": true
}
```

**Respuesta 201:**
```json
{ "id": 5, "name": "Laura Gómez", "email": "laura.gomez@device.com", "role": "support", "is_active": true }
```

**Respuesta 409 (correo duplicado):**
```json
{ "detail": "Ya existe un usuario con el correo 'laura.gomez@device.com'" }
```

**Respuesta 422 (validación fallida — nombre muy corto):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "name"],
      "msg": "Value error, El nombre debe tener mínimo 3 caracteres"
    }
  ]
}
```

---

## Cabeceras HTTP personalizadas

Cada respuesta incluye:

```
X-App-Name: device_systems
X-API-Version: 1.0
```

---

## Validaciones con Pydantic v2

| Campo | Regla |
|-------|-------|
| `name` | Obligatorio, mínimo 3 caracteres |
| `email` | Formato de correo válido (`EmailStr`) |
| `role` | Solo acepta: `admin`, `support`, `user` |
| `is_active` | Booleano (`true`/`false`) |

---

## Documentación interactiva

Con el servidor corriendo, accede a:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── main.py
│   ├── schemas/
│   │   └── user_schema.py
│   └── routes/
│       └── user_routes.py
├── requirements.txt
└── README.md
```

---

## Reflexión sobre FastAPI

FastAPI demostró ser un framework muy productivo para construir APIs REST. La integración nativa con **Pydantic v2** elimina código repetitivo de validación: declarar un modelo es suficiente para obtener validación automática, documentación OpenAPI y serialización. Los **path parameters** y **query parameters** se declaran directamente en la firma de la función, lo que hace el código muy legible. La **documentación Swagger** generada automáticamente acelera enormemente las pruebas durante el desarrollo.
