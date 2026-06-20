from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import Base, engine
from app.routes import user_routes, device_routes, loan_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Systems API",
    description="API REST para gestión de usuarios, dispositivos y préstamos tecnológicos.",
    version="2.0.0",
    contact={"name": "SENA - Ficha 3229209"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Device Systems API v2.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
