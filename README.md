# Device Systems API v2.0

API REST para gestión de usuarios, dispositivos tecnológicos y préstamos.  
Desarrollada con FastAPI, SQLAlchemy, Alembic y SQLite.

**SENA – Ficha 3229209**  
Instructor: Mateo Arroyabe  
Actividad: GA1-220501096-01-AA1-EV10

---

## Tecnologías utilizadas

- Python 3.12
- FastAPI 0.115
- SQLAlchemy 2.0
- Alembic 1.13
- Pydantic v2
- SQLite
- Uvicorn

---

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── main.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── user_model.py
│   │   ├── device_model.py
│   │   └── loan_model.py
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── device_schema.py
│   │   └── loan_schema.py
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── device_routes.py
│   │   └── loan_routes.py
│   ├── services/
│   │   ├── user_service.py
│   │   ├── device_service.py
│   │   └── loan_service.py
│   └── dependencies/
│       └── database_dependency.py
├── alembic/
│   └── versions/
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/andresfelipe2552/device_systems.git
cd device_systems
git checkout device_systems_alembic_relaciones

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones
alembic upgrade head

# 4. Ejecutar la API
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`

---

## Migraciones con Alembic

### Inicializar Alembic
```bash
alembic init alembic
```

### Generar migración automática
```bash
alembic revision --autogenerate -m "create users devices and loans tables"
```

### Aplicar migración
```bash
alembic upgrade head
```

### Ver historial
```bash
alembic history
```

Salida esperada:
```
<base> -> 4b3c3e804199 (head), create users devices and loans tables
```

---

## Modelos y relaciones

### User
| Campo | Tipo | Restricción |
|-------|------|-------------|
| id | Integer | Primary Key |
| name | String | Obligatorio |
| email | String | Único, obligatorio |
| phone | String | Opcional |
| created_at | DateTime | Auto |

### Device
| Campo | Tipo | Restricción |
|-------|------|-------------|
| id | Integer | Primary Key |
| name | String | Obligatorio |
| serial_number | String | Único, obligatorio |
| device_type | String | Obligatorio |
| brand | String | Opcional |
| is_available | Boolean | Default True |
| created_at | DateTime | Auto |

### Loan
| Campo | Tipo | Restricción |
|-------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | FK → users.id |
| device_id | Integer | FK → devices.id |
| loan_date | DateTime | Auto |
| return_date | DateTime | Opcional |
| status | String | active / returned / overdue |

### Relaciones
```python
# User → Loan (One-to-Many)
loans = relationship("Loan", back_populates="user")

# Device → Loan (One-to-Many)
loans = relationship("Loan", back_populates="device")

# Loan → User y Loan → Device (Many-to-One)
user = relationship("User", back_populates="loans")
device = relationship("Device", back_populates="loans")
```

---

## Endpoints disponibles

### Users – `/users`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /users | Listar usuarios (filtro: ?search=) |
| GET | /users/{id} | Obtener usuario por ID |
| POST | /users | Crear usuario |
| PUT | /users/{id} | Actualizar usuario completo |
| PATCH | /users/{id} | Actualizar usuario parcial |
| DELETE | /users/{id} | Eliminar usuario |
| GET | /users/{id}/loans | Préstamos del usuario con detalle |

### Devices – `/devices`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /devices | Listar dispositivos (filtros: device_type, is_available, brand, search) |
| GET | /devices/{id} | Obtener dispositivo por ID |
| POST | /devices | Crear dispositivo |
| PUT | /devices/{id} | Actualizar dispositivo completo |
| PATCH | /devices/{id} | Actualizar dispositivo parcial |
| DELETE | /devices/{id} | Eliminar dispositivo |
| GET | /devices/{id}/loans | Historial de préstamos del dispositivo |

### Loans – `/loans`
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /loans | Listar préstamos (filtros: status, user_email, device_type) |
| GET | /loans/details | Préstamos con JOIN (usuario + dispositivo) |
| GET | /loans/{id} | Obtener préstamo por ID |
| POST | /loans | Crear préstamo |
| PATCH | /loans/{id}/return | Devolver dispositivo |

---

## Ejemplos de uso

### Crear usuario
```bash
POST /users
{
  "name": "Ana Pérez",
  "email": "ana@sena.edu.co",
  "phone": "3001234567"
}
```

### Crear dispositivo
```bash
POST /devices
{
  "name": "Laptop Lenovo ThinkPad",
  "serial_number": "LEN-2024-001",
  "device_type": "laptop",
  "brand": "Lenovo"
}
```

### Crear préstamo
```bash
POST /loans
{
  "user_id": 1,
  "device_id": 1
}
```

### Respuesta de detalle con JOIN
```json
{
  "loan_id": 1,
  "status": "active",
  "loan_date": "2024-01-15T10:00:00",
  "return_date": null,
  "user": {
    "id": 1,
    "name": "Ana Pérez",
    "email": "ana@sena.edu.co"
  },
  "device": {
    "id": 1,
    "name": "Laptop Lenovo ThinkPad",
    "serial_number": "LEN-2024-001",
    "device_type": "laptop"
  }
}
```

### Filtros avanzados
```bash
GET /devices?device_type=laptop
GET /devices?is_available=true
GET /devices?brand=lenovo
GET /devices?search=thinkpad
GET /loans?status=active
GET /loans?user_email=ana@sena.edu.co
GET /loans?device_type=laptop
GET /loans/details?status=active&device_type=laptop
```

### Devolver dispositivo
```bash
PATCH /loans/1/return
```

---

## Manejo de errores

| Caso | Código |
|------|--------|
| Registro creado | 201 Created |
| Consulta exitosa | 200 OK |
| Eliminación exitosa | 204 No Content |
| Recurso no encontrado | 404 Not Found |
| Dato duplicado (email / serial) | 400 Bad Request |
| Dispositivo no disponible | 409 Conflict |
| Préstamo ya devuelto | 409 Conflict |
| Error de validación | 422 Unprocessable Entity |

---

## Documentación Swagger

Con la API corriendo, acceder a:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## Reflexión

Las **migraciones con Alembic** permiten versionar los cambios estructurales de la base de datos de forma controlada y reproducible, evitando pérdida de datos al evolucionar el esquema.

Las **relaciones entre modelos** mediante `ForeignKey` y `relationship` garantizan la integridad referencial, asegurando que cada préstamo siempre pertenezca a un usuario y dispositivo existentes.

Las **consultas con joins y filtros avanzados** (`join`, `ilike`, `and_`, `or_`) permiten obtener información relacionada de múltiples tablas en una sola consulta eficiente, lo cual es fundamental en APIs REST profesionales.
