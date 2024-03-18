from fastapi import FastAPI
# import json
from molinos import generate_windmill_data
# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


molinos = FastAPI()


# @molinos.get("/molinos")
# def get_json_file():
#     # Ruta del archivo JSON
#     json_file_path = "/home/cvp/Entrega-3-iot/data/molinos.json"

#     try:
#         # Leer el contenido del archivo JSON
#         with open(json_file_path, "r") as file:
#             json_data = json.load(file)
#         return json_data
#     except FileNotFoundError:
#         return {"detail": "Archivo JSON no encontrado"}
#     except Exception as e:
#         return {"detail": f"Error al leer el archivo JSON: {str(e)}"}
class DatosMolino(BaseModel):
    mill_id: int
    timestamp: str
    value: dict
    
@molinos.get("/molinos")
def obtener_datos():
    datos = []
    for i in range(10):  # Suponiendo que quieres generar 10 conjuntos de datos
        datos.append(generate_windmill_data(i))
    return datos

# Comando uvicorn main:molinos --reload