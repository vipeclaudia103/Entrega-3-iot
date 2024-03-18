import json
import os
import random
import string
import datetime
import threading

# Definir modelos y ubicaciones constantes para cada molino
info_modelos = [
    {
        "id": 1437,
        "modelo": "G58",
        "ubicacion": "Biota"
    },    
    {
        "id": 9083,
        "modelo": "BS32",
        "ubicacion": "Biota"
    },
    {
        "id": 8740,
        "modelo": "DW33",
        "ubicacion": "Biota"
    },    
    {
        "id": 4524,
        "modelo": "PC21",
        "ubicacion": "Biota"
    },
    {
        "id": 7823,
        "modelo": "G58",
        "ubicacion": "Valle de Peraleda"
    },        
    {
        "id": 6843,
        "modelo": "G58",
        "ubicacion": "Valle de Peraleda"
    },    
    {
        "id": 3931,
        "modelo": "BS32",
        "ubicacion": "Merindad"
    },
    {
        "id": 2938,
        "modelo": "G58",
        "ubicacion": "Merindad"
    },    
    {
        "id": 4323,
        "modelo": "PC21",
        "ubicacion": "Lorbes"
    },
    {
        "id": 7465,
        "modelo": "G58",
        "ubicacion": "Lorbes"
    }
]

def letras_aleatorias():
    return ''.join(random.choices(string.ascii_letters, k=3))

def generate_windmill_data(mill_id):
    """
    Función para generar datos simulados de un molino de viento.
    """
    timestamp = datetime.datetime.now().isoformat()
    wind_speed = round(random.uniform(0, 25), 2)  # Velocidad del viento en m/s
    power_output = round(random.uniform(0, 100), 2)  # Salida de energía en watts
    
    # --- Probabilidad de datos erroneos -----
    p_error = random.uniform(0, 100)
    if p_error < 25:
        wind_speed *= -2
    elif p_error > 80:
        power_output = letras_aleatorias()  # Devuelve 3 letras aleatorias en lugar de números
    
    # Obtener modelo y ubicación para el molino
    id = info_modelos[mill_id]["id"]
    modelo = info_modelos[mill_id]["modelo"]
    ubicacion = info_modelos[mill_id]["ubicacion"]

    data = {
        "mill_id": mill_id,
        "id": id,
        "model": modelo,
        "location": ubicacion,
        "timestamp": timestamp,
        "value": {
            "wind_speed": wind_speed,
            "power_output": power_output
        }
    }

    return data

def save_data_to_json(data, filename):
    """
    Función para guardar datos en un archivo JSON.
    """
    # Comprobar si el directorio existe, si no, crearlo
    if not os.path.exists(filename):
        os.makedirs(filename)
    
    # Escribir los datos en el archivo molinos.json dentro del directorio
    with open(os.path.join(filename, "molinos.json"), "a") as file:
        file.write(data + "\n")

def generar_periodicamente():
    global ESPERA
    t = threading.Timer(ESPERA, generar_periodicamente)
    t.start()
    
    global NUM_MOLINOS
    for i in range(NUM_MOLINOS):
        datos = generate_windmill_data(i)
        directory = "/home/cvp/Entrega-3-iot/data"
        # save_data_to_json(datos, directory)

NUM_MOLINOS = 10
ESPERA = 10
generar_periodicamente()
