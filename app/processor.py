# processor.py
import os
import json
import re
from collections import defaultdict
from google.cloud import storage

def leer_logs_gcs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    contenido = blob.download_as_text()
    return contenido.splitlines()

def obtener_severidad(log):
    match = re.match(r"^\[(ERROR|WARNING|INFO)\]", log)
    if match:
        return match.group(1)
    return "UNKNOWN"

def agrupar_logs_por_severidad(logs):
    logs_por_severidad = defaultdict(list)
    for log in logs:
        severidad = obtener_severidad(log)
        logs_por_severidad[severidad].append(log.strip())
    return logs_por_severidad

def guardar_logs_agrupados_en_gcs(logs_agrupados, bucket_name, output_file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(output_file_name)
    blob.upload_from_string(json.dumps(logs_agrupados, indent=4))

def procesar_logs():
    bucket_name = os.environ["BUCKET_NAME"]
    file_name = os.environ["FILE_NAME"]
    logs = leer_logs_gcs(bucket_name, file_name)
    logs_agrupados = agrupar_logs_por_severidad(logs)
    nombre_salida = file_name.replace(".txt", "_agrupado.json")
    output_path = f"procesado/{nombre_salida}"
    guardar_logs_agrupados_en_gcs(logs_agrupados, bucket_name, output_path)
    print(f"Logs procesados y guardados en: {output_path}")
    return {
        "mensaje": "Procesamiento completo",
        "archivo_salida": output_path
    }

