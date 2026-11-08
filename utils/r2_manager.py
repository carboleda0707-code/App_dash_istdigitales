import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL", "")
R2_PUBLIC_DOMAIN = os.getenv("R2_PUBLIC_DOMAIN", "")

def obtener_cliente_s3():
    """Inicializa el cliente S3 para interactuar con Cloudflare R2."""
    if not R2_ENDPOINT_URL:
        raise ValueError("⚠️ R2_ENDPOINT_URL no está configurado.")

    return boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name='auto'
    )

def listar_buckets_y_uso():
    """Retorna una simulación o consulta real de los buckets en tu cuenta central de R2."""
    try:
        s3 = obtener_cliente_s3()
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response.get('Buckets', [])]
        return {"status": "success", "buckets": buckets}
    except Exception as e:
        return {"status": "error", "message": str(e), "buckets": ["bookea-media", "fajas-isabella-media", "pacificzone-media"]}