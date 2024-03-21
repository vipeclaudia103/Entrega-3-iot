# Comando uvicorn main:molinos --reload
# Importaciones necesarias para el manejo de la API y la validación de datos
from typing import Dict, Union
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, validator

# Inicialización de la aplicación FastAPI
molinos = FastAPI()

# Definición del modelo de datos para los registros de los molinos
class DatosMolino(BaseModel):
    mill_id: int
    id: int
    model: str
    location: str
    timestamp: str
    value: Dict[str, float]

    # Validador personalizado para los valores en value
    @validator("value")
    def validar_value(cls, v, values, **kwargs):
        mill_id = values.get("mill_id")
        try:
            # Validación de cada clave y valor en value
            for key, val in v.items():
                if isinstance(val, str):
                    raise ValueError(f"{mill_id}: El valor de '{key}' no puede ser una cadena")
                # Validación específica para cada tipo de valor
                if key == 'velocidad_viento' and (val < 0 or val > 25):
                    raise ValueError(f"{mill_id}: El valor de '{key}' debe estar entre 0 y 25")
                if key == 'direccion_viento' and (val < 0 or val > 360):
                    raise ValueError(f"{mill_id}: El valor de '{key}' debe estar entre 0 y 360")
                if key == 'produccion_energia' and (val < 0 or val > 1000):
                    raise ValueError(f"{mill_id}: El valor de '{key}' debe estar entre 0 y 1000")
                if key == 'temperatura_ambiente' and (val < -10 or val > 40):
                    raise ValueError(f"{mill_id}: El valor de '{key}' debe estar entre -10 y 40")
                if key == 'humedad' and (val < 0 or val > 100):
                    raise ValueError(f"{mill_id}: El valor de '{key}' debe estar entre 0 y 100")
                if key == 'presion_atmosferica' and (val < 900 or val > 1100):
                    raise ValueError(f"{mill_id}: El valor de '{key}' debe estar entre 900 y 1100")
                if key == 'vibraciones' and (val < 0 or val > 5):
                    raise ValueError(f"{mill_id}: El valor de '{key}' debe estar entre 0 y 5")
        except ValueError as e:
            print(e)
        return v

# Función para calcular las medias de los datos de los molinos
def calcular_medias(molinos_generados, origen):
    if isinstance(molinos_generados, list):
        total_molinos = len(molinos_generados)
        
        if total_molinos == 0:
            # Si no hay datos de molinos, devuelve un mensaje indicando que no hay datos disponibles
            return {"message": "No hay datos de molinos disponibles"}
        
        # Calcula las medias de los diferentes parámetros de los molinos
        medias = {
            "Media sobre": origen,  # Origen de los datos para la media
            "media_velocidad_viento": sum(m.value.get('velocidad_viento', 0) for m in molinos_generados) / total_molinos,
            "media_direccion_viento": sum(m.value.get('direccion_viento', 0) for m in molinos_generados) / total_molinos,
            "media_produccion_energia": sum(m.value.get('produccion_energia', 0) for m in molinos_generados) / total_molinos,
            "media_temperatura_ambiente": sum(m.value.get('temperatura_ambiente', 0) for m in molinos_generados) / total_molinos,
            "media_humedad": sum(m.value.get('humedad', 0) for m in molinos_generados) / total_molinos,
            "media_presion_atmosferica": sum(m.value.get('presion_atmosferica', 0) for m in molinos_generados) / total_molinos,
            "media_vibraciones": sum(m.value.get('vibraciones', 0) for m in molinos_generados) / total_molinos,
        }
        
        return medias
    else:
        # Si los datos de entrada no son una lista, devuelve un mensaje indicando que la entrada no es válida
        return {"message": "La entrada no es una lista"}

# Lista para almacenar los datos de los molinos
datos_molinos = []

# Endpoint POST para subir datos de los molinos
@molinos.post("/datos-molinos/")
def subir_datos(datos: DatosMolino):
    # Agregar los datos a la lista
    datos_molinos.append(datos)
    return datos

# Endpoints para obtener medias de los datos de los molinos

@molinos.get("/medias-global", response_model=Dict[str, Union[float, str]])
def obtener_medias():
    """
    Endpoint para obtener las medias globales de todos los molinos generados.
    """
    # Obtiene los datos generados y calcula las medias    
    return calcular_medias(datos_molinos, "Todos los molinos")

@molinos.get("/media-ubi/{ubicacion}", response_model=Dict[str, Union[float, str]])
def obtener_media_por_ubicacion(ubicacion: str):
    """
    Endpoint para obtener las medias de los molinos ubicados en una ubicación específica.
    """
    # Obtiene los datos generados y filtra por ubicación
    molinos_generados_ubicacion = [m for m in datos_molinos if m.location == ubicacion]
    if not molinos_generados_ubicacion:
        # Si no hay datos para la ubicación especificada, devuelve un error 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron datos para la ubicación {ubicacion}")
    # Devuelve las medias como un diccionario
    return calcular_medias(molinos_generados_ubicacion, ubicacion)

@molinos.get("/media-modelo/{modelo}", response_model=Dict[str, Union[float, str]])
def obtener_media_por_modelo(modelo: str):
    """
    Endpoint para obtener las medias de los molinos de un modelo específico.
    """
    # Obtiene los datos generados y filtra por modelo
    molinos_generados_modelo = [m for m in datos_molinos if m.model == modelo]
    
    if not molinos_generados_modelo:
        # Si no hay datos para el modelo especificado, devuelve un error 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron datos para la modelo {modelo}")
    # Devuelve las medias como un
    return calcular_medias(molinos_generados_modelo, modelo)

@molinos.get("/media-mill_id/{mill_id}", response_model=Dict[str, Union[float, str]])
def obtener_media_por_mill_id(mill_id: int):
    """
    Endpoint para obtener las medias de un molino específico identificado por su ID de molino.
    """
    # Obtiene los datos generados y filtra por mill_id
    molinos_generados_mill_id = [m for m in datos_molinos if m.mill_id == mill_id]
    
    if not molinos_generados_mill_id:
        # Si no hay datos para el ID de molino especificado, devuelve un error 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron datos para la mill_id {mill_id}")
    # Devuelve las medias como un diccion
    return calcular_medias(molinos_generados_mill_id, mill_id)