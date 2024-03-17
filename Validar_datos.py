from fastapi import FastAPI
from typing import List
import random
import datetime

# Importamos las funciones que generan y guardan los datos
from Generador_datos import generate_multiple_windmill_data, save_data_to_json

app = FastAPI()

# Cargamos los datos de los molinos desde el archivo JSON
def load_data():
    with open("windmill_data.json", "r") as json_file:
        data = json.load(json_file)
    return data

# Obtener datos de todos los molinos
@app.get("/windmills/", response_model=List[dict])
async def get_windmill_data():
    return load_data()

# Obtener datos de un molino específico
@app.get("/windmills/{mill_id}", response_model=dict)
async def get_windmill_data_by_id(mill_id: str):
    data = load_data()
    for mill_data in data:
        if mill_data["mill_id"] == mill_id:
            return mill_data
    return {"message": "Molino no encontrado"}

if __name__ == "__main__":
    # Generamos datos simulados y los guardamos en el archivo JSON
    num_mills = 3  # Número de molinos de viento
    mills_data = generate_multiple_windmill_data(num_mills)
    save_data_to_json(mills_data, "windmill_data.json")

    # Ejecutamos el servidor de FastAPI
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
