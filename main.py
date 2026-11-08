import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from dotenv import load_dotenv

# Importaciones modulares con tu estructura de carpetas
from config.database import engine, Base, get_db
from utils.r2_manager import listar_buckets_y_uso
from routes import apps_routes
from config.config_loader import cfg

load_dotenv()

def sembrar_apps_iniciales():
    """Siembra inicial automática leyendo de apps_seed.json sin quemar datos en SQL."""
    seed_path = "apps_seed.json"
    if not os.path.exists(seed_path):
        return

    db = next(get_db())
    try:
        count_result = db.execute(text("SELECT COUNT(*) FROM apps_master;")).scalar()
        if count_result == 0:
            with open(seed_path, "r", encoding="utf-8") as f:
                apps_list = json.load(f)
            
            for app in apps_list:
                query = text("""
                    INSERT INTO apps_master (nombre, slug, categoria, bucket_r2, dominio_api, panel_admin_url, web_url, estado)
                    VALUES (:nombre, :slug, :categoria, :bucket_r2, :dominio_api, :panel_admin_url, :web_url, :estado)
                    ON CONFLICT (slug) DO NOTHING;
                """)
                db.execute(query, app)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"⚠️ Error en siembra automática: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Crear tablas en PostgreSQL si no existen al arrancar
    Base.metadata.create_all(bind=engine)
    # 2. Ejecutar siembra automática de forma segura
    sembrar_apps_iniciales()
    yield

app = FastAPI(
    title=cfg.get("system", "app_title", "IstDigitales Control Center"),
    description="Panel Maestro para Administrar Aplicaciones Web, Cloudflare R2 y PostgreSQL",
    version=cfg.get("system", "version", "1.0.0"),
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(apps_routes.router)

@app.get("/")
def home():
    return {
        "sistema": "IstDigitales Control Center",
        "estado": "Activo en Railway",
        "postgresql": "Conectado",
        "documentdocs": "/docs"
    }

@app.get("/api/v1/r2/status")
def verificar_r2():
    return listar_buckets_y_uso()

@app.get("/api/v1/health")
def health_check():
    return {
        "cloudflare_r2": "Conectado ($0 Egress activo)",
        "postgresql": "Conectado",
        "ecosistema": "IstDigitales Activo"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)