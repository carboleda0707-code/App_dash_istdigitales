from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from sqlalchemy import text

router = APIRouter(prefix="/api/apps", tags=["Aplicaciones IstDigitales"])

@router.get("/")
def listar_apps(db: Session = Depends(get_db)):
    """Lista todas las aplicaciones registradas en el ecosistema."""
    try:
        query = text("SELECT id, nombre, slug, categoria, bucket_r2, dominio_api, panel_admin_url, web_url, estado, storage_used_mb FROM apps_master;")
        result = db.execute(query).fetchall()
        
        apps = []
        for row in result:
            apps.append({
                "id": row[0],
                "nombre": row[1],
                "slug": row[2],
                "categoria": row[3],
                "bucket_r2": row[4],
                "dominio_api": row[5],
                "panel_admin_url": row[6],
                "web_url": row[7],
                "estado": row[8],
                "storage_used_mb": float(row[9]) if row[9] else 0.0
            })
        return {"total": len(apps), "applications": apps}
    except Exception as e:
        # Fallback de prueba si la base de datos aún no tiene la tabla creada
        return {
            "total": 3,
            "applications": [
                {"id": 1, "nombre": "Bookea EC", "slug": "bookea", "categoria": "Reservas", "bucket_r2": "bookea-media", "estado": "activo"},
                {"id": 2, "nombre": "Fajas Isabella", "slug": "fajas-isabella", "categoria": "E-commerce", "bucket_r2": "fajas-isabella-media", "estado": "activo"},
                {"id": 3, "nombre": "PacificZone", "slug": "pacificzone", "categoria": "Catálogo", "bucket_r2": "pacificzone-media", "estado": "activo"}
            ]
        }