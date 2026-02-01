"""
Main FastAPI application for testing
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.infrastructure.db.database import get_db

app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "service": settings.app_name,
        "status": "running"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Проверка здоровья сервиса"""
    try:
        # Проверяем подключение к БД
        db.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "database": "connected",
            "service": settings.app_name
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

@app.get("/db-info")
def db_info():
    """Информация о подключении к БД"""
    return {
        "database_url": settings.database_url,
        "db_host": settings.db_host,
        "db_name": settings.db_name
    }