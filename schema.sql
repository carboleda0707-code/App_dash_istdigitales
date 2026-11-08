CREATE TABLE IF NOT EXISTS apps_master (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    categoria VARCHAR(50) DEFAULT 'ecommerce',
    bucket_r2 VARCHAR(100) NOT NULL,
    dominio_api VARCHAR(255) NOT NULL,
    panel_admin_url VARCHAR(255),
    web_url VARCHAR(255),
    estado VARCHAR(20) DEFAULT 'activo',
    storage_used_mb NUMERIC(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla lista. Los datos iniciales se alimentan dinámicamente desde apps_seed.json al arrancar la API.