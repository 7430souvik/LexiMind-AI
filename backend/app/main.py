from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.session import engine

from app.auth.router import router as auth_router

from app.documents.router import router as document_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(document_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to LexiMind AI 🚀"
    }


@app.get("/health")
def health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }


