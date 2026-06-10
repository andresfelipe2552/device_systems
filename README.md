# device_systems API — v2.0

API REST para la **gestión de usuarios** del sistema `device_systems`, construida con **FastAPI**, **SQLAlchemy** y validaciones **Pydantic v2**.

---

## Descripción

`device_systems` v2.0 evoluciona la versión anterior (datos en memoria) para incorporar **persistencia real** mediante una base de datos SQLite gestionada con SQLAlchemy. Expone un CRUD completo sobre el recurso `/users`.

---

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── main.py                          # Punto de entrada FastAPI
│   ├── database/
│   │   └── connection.py                # Engine, SessionLocal, Base, create_tables()
│   ├── models/
│   │   └── user_model.py                # Modelo SQLAlchemy → tabla 'users'
│   ├── schemas/
│   │   └── user_schema.py               # Schemas Pydantic: Create, Update, Patch, Response
│   ├── routes/
│   │   └── user_routes.py               # Endpoints REST del recurso /users
│   ├── services/
│   │   └── user_service.py              # Lógica CRUD sobre la base de datos
│   └── dependencies/
│       └── database_dependency.py       # Dependencia get_db() para inyección de sesión
├── requirements.txt
└── README.md
```

---

## Instalación

```bash
git clone https://github.com/andresfelipe2552/device_systems.git
cd device_systems

python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

---

## Ejecución

```bash
uvicorn app.main:app --reload
```

Servidor disponible en: `http://127.0.0.1:8000`

> La base de datos `device_systems.db` se crea automáticamente al iniciar.

---

## Endpoints

| Método   | Ruta                  | Descripción                               | Código éxito |
|----------|-----------------------|-------------------------------------------|--------------|
| `GET`    | `/users`              | Listar usuarios (con filtros y orden)     | 200          |
| `GET`    | `/users/{user_id}`    | Obtener usuario por ID                    | 200          |
| `POST`   | `/users`              | Crear nuevo usuario                       | 201          |
| `PUT`    | `/users/{user_id}`    | Actualizar usuario completo               | 200          |
| `PATCH`  | `/users/{user_id}`    | Actualizar usuario parcialmente           | 200          |
| `DELETE` | `/users/{user_id}`    | Eliminar usuario                          | 204          |

### Parámetros de query en GET /users

| Parámetro  | Tipo    | Descripción                                  |
|------------|---------|----------------------------------------------|
| `role`     | string  | Filtrar por rol: `admin`, `support`, `user`  |
| `is_active`| boolean | Filtrar por estado: `true` / `false`         |
| `order_by` | string  | Ordenar por: `name` / `created_at`           |

---

## Manejo de errores

| Caso                          | Código |
|-------------------------------|--------|
| Usuario creado                | 201    |
| Consulta / actualización OK   | 200    |
| Eliminación exitosa           | 204    |
| Usuario no encontrado         | 404    |
| Email duplicado               | 400    |
| order_by inválido             | 400    |
| Error de validación Pydantic  | 422    |

---

## Validaciones (Pydantic v2)

| Campo       | Regla                                        |
|-------------|----------------------------------------------|
| `name`      | Obligatorio, mínimo 3 caracteres             |
| `email`     | Formato válido (`EmailStr`)                  |
| `role`      | Solo acepta: `admin`, `support`, `user`      |
| `is_active` | Booleano (`true` / `false`)                  |

---

## Modelo SQLAlchemy vs Schema Pydantic

| Aspecto          | Modelo SQLAlchemy (`user_model.py`)              | Schema Pydantic (`user_schema.py`)                   |
|------------------|--------------------------------------------------|------------------------------------------------------|
| **Propósito**    | Representa la tabla en la base de datos          | Valida y serializa datos de entrada/salida de la API |
| **Uso**          | ORM: consultas, inserciones, relaciones          | Contratos de la API: request body y response         |
| **Validaciones** | Constraints de BD: `nullable`, `unique`, `index` | Reglas de negocio: longitud, formato, enum           |
| **Ejemplo**      | `Column(String, unique=True, nullable=False)`    | `email: EmailStr`, `@field_validator`                |

> **Clave:** el modelo ORM habla con la base de datos; el schema Pydantic habla con el cliente HTTP. Son capas separadas por diseño.

---

## Cabeceras HTTP personalizadas

Cada respuesta incluye:

```
X-App-Name: device_systems
X-API-Version: 2.0
```

---

## Documentación interactiva

Con el servidor corriendo:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:**      `http://127.0.0.1:8000/redoc`

---

## Reflexión — Importancia de la persistencia

La versión anterior almacenaba usuarios en listas Python que se perdían al reiniciar el servidor, lo que hace imposible cualquier uso real. Incorporar SQLAlchemy transforma la API en un sistema confiable: los datos sobreviven reinicios, se pueden consultar con filtros eficientes gracias a índices, y se garantiza integridad mediante constraints (`unique`, `nullable=False`). La separación entre modelo ORM y schema Pydantic también hace el código más mantenible: cada capa tiene una responsabilidad clara y se puede modificar de forma independiente.
