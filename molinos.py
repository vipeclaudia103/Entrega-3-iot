import json
import os
import random
import string
import datetime
import threading

import requests

# Definir modelos y ubicaciones constantes para cada molino
info_modelos = [
    {
        "id": 1437,
        "modelo": "G58",
        "ubicacion": "Biota Zona Norte"
    },    
    {
        "id": 9083,
        "modelo": "BS32",
        "ubicacion": "Biota Zona Sur"
    },
    {
        "id": 8740,
        "modelo": "DW33",
        "ubicacion": "Biota Zona Oeste"
    },    
    {
        "id": 4524,
        "modelo": "PC21",
        "ubicacion": "Biota Zona Sur"
    },
    {
        "id": 7823,
        "modelo": "G58",
        "ubicacion": "Biota Zona Este"
    },        
    {
        "id": 6843,
        "modelo": "G58",
        "ubicacion": "Biota Zona Norte"
    },    
    {
        "id": 3931,
        "modelo": "BS32",
        "ubicacion": "Biota Zona Sur"
    },
    {
        "id": 2938,
        "modelo": "G58",
        "ubicacion": "Biota Zona Oeste"
    },    
    {
        "id": 4323,
        "modelo": "PC21",
        "ubicacion": "Biota Zona Central"
    },
    {
        "id": 7465,
        "modelo": "G58",
        "ubicacion": "Biota Zona Este"
    }
]

def generate_windmill_data(mill_id, probabilidad_error):
    """
    Función para generar datos simulados de un molino de viento.
    """
    timestamp = datetime.datetime.now().isoformat()
    velocidad_viento = round(random.uniform(0, 25), 2)  # Velocidad del viento en m/s
    direccion_viento = round(random.uniform(0, 360), 2)  # Dirección del viento en grados
    produccion_energia = round(random.uniform(0, 1000), 2)  # Producción de energía en kW
    temperatura_ambiente = round(random.uniform(-10, 40), 2)  # Temperatura ambiente en °C
    humedad = round(random.uniform(0, 100), 2)  # Humedad relativa en %
    presion_atmosferica = round(random.uniform(900, 1100), 2)  # Presión atmosférica en hPa
    vibraciones = round(random.uniform(0, 5), 2)  # Nivel de vibraciones en mm/s^2
    
    
    # --- Probabilidad de datos erroneos -----
    error = False
    e_mj = ""
    # Aplicar posibles errores

    if random.random() <  probabilidad_error:
        velocidad_viento *= -1    # Vuelve la velocidad negativa 
        error = True
        e_mj += "\nError de velocidad_viento"
    elif random.random() <  probabilidad_error:
        produccion_energia *= -0.5  # Devuelve 3 letras aleatorias en lugar de números
        error = True
        e_mj += "\nError de produccion_energia"
    elif random.random() <  probabilidad_error:
        temperatura_ambiente *= 100     # Eleva la temperatura por 100
        error = True
        e_mj += "\nError de temperatura_ambiente"
    elif random.random() <  probabilidad_error:
        direccion_viento *= -0.5  # Devuelve 3 letras aleatorias en lugar de números
        error = True
        e_mj += "\nError de direccion_viento"
    elif random.random() <  probabilidad_error:
        presion_atmosferica *= -20     # Disminuye la presión 20 veces
        error = True
        e_mj += "\nError de presion_atmosferica"
    elif random.random() <  probabilidad_error:
        humedad *= -0.5  # Devuelve 3 letras aleatorias en lugar de números
        error = True
        e_mj += "\nError de humedad"
    elif random.random() <  probabilidad_error:
        vibraciones *= -0.5
        error = True
        e_mj += "\nError de vibraciones"
    if error:
        mensaje = "{}: {}".format(mill_id,e_mj)
        print(mensaje)


 
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
            "velocidad_viento": velocidad_viento,
            "direccion_viento": direccion_viento,
            "produccion_energia":produccion_energia,
            "temperatura_ambiente": temperatura_ambiente,
            "humedad": humedad,
            "presion_atmosferica": presion_atmosferica,
            "vibraciones": vibraciones
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
        file.write(json.dumps(data) + "\n")

def generar_periodicamente():
    global ESPERA
    t = threading.Timer(ESPERA, generar_periodicamente)
    t.start()
    
    global NUM_MOLINOS
    for i in range(NUM_MOLINOS):
        global p_error
        new_data = generate_windmill_data(i, p_error)
        url_post = "http://127.0.0.1:8000/datos-molinos/"
        # A POST request to tthe API
        post_response = requests.post(url_post, json=new_data)
            # Print the response
        post_response_json = post_response.json()
        print(post_response_json)
        # Guardar datos
        # directory = "/home/cvp/Entrega-3-iot/data"
        # save_data_to_json(new_data, directory)

NUM_MOLINOS = 10
ESPERA = 10
p_error = 0.1
generar_periodicamente()
