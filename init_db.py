import os
import json
from sqlalchemy import text
from config.database import engine, Base, SessionLocal
# Importa tus modelos aquí para que SQLAlchemy los reconozca (ej. from models import AppModel)

def inicializar_base_datos():
    print("🔄 Verificando e inicializando base de datos PostgreSQL...")
    try:
        # 1. Crear tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas verificadas/creadas correctamente.")

        # 2. Sembrar datos desde apps_seed.json
        seed_path = "apps_seed.json"
        if os.path.exists(seed_path):
            db = SessionLocal()
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
                    print("🌱 Datos iniciales sembrados exitosamente desde apps_seed.json.")
                else:
                    print("ℹ️ La tabla apps_master ya contiene registros.")
            except Exception as e:
                db.rollback()
                print(f"⚠️ Error durante la siembra: {e}")
            finally:
                db.close()
    except Exception as e:
        print(f"❌ Error crítico conectando a PostgreSQL: {e}")

if __name__ == "__main__":
    inicializar_base_datos()