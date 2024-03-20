# Comando uvicorn main:molinos --reload
from typing import Dict
from fastapi import FastAPI,  HTTPException, status
from pydantic import BaseModel, validator

molinos = FastAPI()

class DatosMolino(BaseModel):
    mill_id: int
    id: int
    model: str
    location: str
    timestamp: str
    value: Dict[str, float]

    @validator("value")
    def validar_value(cls, v):
        try:
            for key, val in v.items():
                if isinstance(val, str):
                    raise ValueError(f"El valor de '{key}' no puede ser una cadena")
                if key == 'velocidad_viento' and (val < 0 or val > 25):
                    raise ValueError(f"El valor de '{key}' debe estar entre 0 y 25")
                if key == 'direccion_viento' and (val < 0 or val > 360):
                    raise ValueError(f"El valor de '{key}' debe estar entre 0 y 360")
                if key == 'produccion_energia' and (val < 0 or val > 1000):
                    raise ValueError(f"El valor de '{key}' debe estar entre 0 y 1000")
                if key == 'temperatura_ambiente' and (val < -10 or val > 40):
                    raise ValueError(f"El valor de '{key}' debe estar entre -10 y 40")
                if key == 'humedad' and (val < 0 or val > 100):
                    raise ValueError(f"El valor de '{key}' debe estar entre 0 y 100")
                if key == 'presion_atmosferica' and (val < 900 or val > 1100):
                    raise ValueError(f"El valor de '{key}' debe estar entre 900 y 1100")
                if key == 'vibraciones' and (val < 0 or val > 5):
                    raise ValueError(f"El valor de '{key}' debe estar entre 0 y 5")
        except ValueError as e:
            print(e)
        return v


# Lista para almacenar los datos de los molinos
datos_molinos = []
# Endpoint POST para subir datos de los molinos
@molinos.post("/datos-molinos/")
def subir_datos(datos: DatosMolino):
    # Agregar los datos a la lista
    datos_molinos.append(datos)
    return datos

@molinos.get("/medias-global", response_model=Dict[str, float])
def obtener_medias():
    # Obtiene los datos generados y calcula las medias
    molinos_generados = datos_molinos
    
    if isinstance(molinos_generados, list):
        total_molinos = len(molinos_generados)
        
        if total_molinos == 0:
            return {"message": "No hay datos de molinos disponibles"}
        
        # Calcula las medias
        medias = {
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
        return {"message": "No se pudieron obtener los datos de los molinos"}




@molinos.get("/media-ubi/{ubicacion}", response_model=Dict[str, float])
def obtener_media_por_ubicacion(ubicacion: str):
    # Obtiene los datos generados y filtra por ubicación
    molinos_generados_ubicacion = [m for m in datos_molinos if m.location == ubicacion]
    
    if not molinos_generados_ubicacion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron datos para la ubicación {ubicacion}")
    
    total_molinos_ubicacion = len(molinos_generados_ubicacion)
    
    # Calcula las sumas de cada atributo
    suma_velocidad_viento = sum(m.value['velocidad_viento'] for m in molinos_generados_ubicacion)
    suma_direccion_viento = sum(m.value['direccion_viento'] for m in molinos_generados_ubicacion)
    suma_produccion_energia = sum(m.value['produccion_energia'] for m in molinos_generados_ubicacion)
    suma_temperatura_ambiente = sum(m.value['temperatura_ambiente'] for m in molinos_generados_ubicacion)
    suma_humedad = sum(m.value['humedad'] for m in molinos_generados_ubicacion)
    suma_presion_atmosferica = sum(m.value['presion_atmosferica'] for m in molinos_generados_ubicacion)
    suma_vibraciones = sum(m.value['vibraciones'] for m in molinos_generados_ubicacion)
    
    # Calcula las medias
    media_velocidad_viento = suma_velocidad_viento / total_molinos_ubicacion
    media_direccion_viento = suma_direccion_viento / total_molinos_ubicacion
    media_produccion_energia = suma_produccion_energia / total_molinos_ubicacion
    media_temperatura_ambiente = suma_temperatura_ambiente / total_molinos_ubicacion
    media_humedad = suma_humedad / total_molinos_ubicacion
    media_presion_atmosferica = suma_presion_atmosferica / total_molinos_ubicacion
    media_vibraciones = suma_vibraciones / total_molinos_ubicacion
    
    # Devuelve las medias como un diccionario
    return {
        "media_velocidad_viento": media_velocidad_viento,
        "media_direccion_viento": media_direccion_viento,
        "media_produccion_energia": media_produccion_energia,
        "media_temperatura_ambiente": media_temperatura_ambiente,
        "media_humedad": media_humedad,
        "media_presion_atmosferica": media_presion_atmosferica,
        "media_vibraciones": media_vibraciones
    }

@molinos.get("/media-modelo/{modelo}", response_model=Dict[str, float])
def obtener_media_por_modelo(modelo: str):
    # Obtiene los datos generados y filtra por modelo
    molinos_generados_modelo = [m for m in datos_molinos if m.model == modelo]
    
    if not molinos_generados_modelo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontraron datos para la modelo {modelo}")
    
    total_molinos_modelo = len(molinos_generados_modelo)
    
    # Calcula las sumas de cada atributo
    suma_velocidad_viento = sum(m.value['velocidad_viento'] for m in molinos_generados_modelo)
    suma_direccion_viento = sum(m.value['direccion_viento'] for m in molinos_generados_modelo)
    suma_produccion_energia = sum(m.value['produccion_energia'] for m in molinos_generados_modelo)
    suma_temperatura_ambiente = sum(m.value['temperatura_ambiente'] for m in molinos_generados_modelo)
    suma_humedad = sum(m.value['humedad'] for m in molinos_generados_modelo)
    suma_presion_atmosferica = sum(m.value['presion_atmosferica'] for m in molinos_generados_modelo)
    suma_vibraciones = sum(m.value['vibraciones'] for m in molinos_generados_modelo)
    
    # Calcula las medias
    media_velocidad_viento = suma_velocidad_viento / total_molinos_modelo
    media_direccion_viento = suma_direccion_viento / total_molinos_modelo
    media_produccion_energia = suma_produccion_energia / total_molinos_modelo
    media_temperatura_ambiente = suma_temperatura_ambiente / total_molinos_modelo
    media_humedad = suma_humedad / total_molinos_modelo
    media_presion_atmosferica = suma_presion_atmosferica / total_molinos_modelo
    media_vibraciones = suma_vibraciones / total_molinos_modelo
    
    # Devuelve las medias como un diccionario
    return {
        "media_velocidad_viento": media_velocidad_viento,
        "media_direccion_viento": media_direccion_viento,
        "media_produccion_energia": media_produccion_energia,
        "media_temperatura_ambiente": media_temperatura_ambiente,
        "media_humedad": media_humedad,
        "media_presion_atmosferica": media_presion_atmosferica,
        "media_vibraciones": media_vibraciones
    }

