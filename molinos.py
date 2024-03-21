import random
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
        "modelo": "SG 14-222 DD",
        "ubicacion": "Biota Zona Sur"
    },
    {
        "id": 8740,
        "modelo": "V164-9.5 MW",
        "ubicacion": "Biota Zona Oeste"
    },    
    {
        "id": 4524,
        "modelo": "EP3",
        "ubicacion": "Biota Zona Sur"
    },
    {
        "id": 7823,
        "modelo": "V164-9.5 MW",
        "ubicacion": "Biota Zona Este"
    },        
    {
        "id": 6843,
        "modelo": "N149",
        "ubicacion": "Biota Zona Norte"
    },    
    {
        "id": 3931,
        "modelo": "SG 14-222 DD",
        "ubicacion": "Biota Zona Sur"
    },
    {
        "id": 2938,
        "modelo": "N149",
        "ubicacion": "Biota Zona Oeste"
    },    
    {
        "id": 4323,
        "modelo": "EP3",
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
    # Generar una marca de tiempo actual en formato ISO
    timestamp = datetime.datetime.now().isoformat()
    
    # Generar datos aleatorios para diferentes parámetros del molino
    velocidad_viento = round(random.uniform(0, 25), 2)  # Velocidad del viento en m/s
    direccion_viento = round(random.uniform(0, 360), 2)  # Dirección del viento en grados
    produccion_energia = round(random.uniform(0, 1000), 2)  # Producción de energía en kW
    temperatura_ambiente = round(random.uniform(-10, 40), 2)  # Temperatura ambiente en °C
    humedad = round(random.uniform(0, 100), 2)  # Humedad relativa en %
    presion_atmosferica = round(random.uniform(900, 1100), 2)  # Presión atmosférica en hPa
    vibraciones = round(random.uniform(0, 5), 2)  # Nivel de vibraciones en mm/s^2
    
    # Probabilidad de introducir errores en los datos
    error = False
    e_mj = ""
    if random.random() < probabilidad_error:
        velocidad_viento *= -1    # Hacer que la velocidad del viento sea negativa 
        error = True
        e_mj += "\nError de velocidad_viento"
    elif random.random() < probabilidad_error:
        produccion_energia *= -0.5  # Introducir un error en la producción de energía
        error = True
        e_mj += "\nError de produccion_energia"
    elif random.random() < probabilidad_error:
        temperatura_ambiente *= 100     # Eleva la temperatura ambiental
        error = True
        e_mj += "\nError de temperatura_ambiente"
    elif random.random() < probabilidad_error:
        direccion_viento *= -0.5  # Introducir un error en la dirección del viento
        error = True
        e_mj += "\nError de direccion_viento"
    elif random.random() < probabilidad_error:
        presion_atmosferica *= -20     # Reducir la presión atmosférica
        error = True
        e_mj += "\nError de presion_atmosferica"
    elif random.random() < probabilidad_error:
        humedad *= -0.5  # Introducir un error en la humedad
        error = True
        e_mj += "\nError de humedad"
    elif random.random() < probabilidad_error:
        vibraciones *= -0.5  # Introducir un error en las vibraciones
        error = True
        e_mj += "\nError de vibraciones"
    if error:
        # Si hay un error, imprimir un mensaje indicando el ID del molino y el tipo de error
        mensaje = "{}: {}".format(mill_id, e_mj)
        print(mensaje)

    # Obtener modelo y ubicación para el molino
    id = info_modelos[mill_id]["id"]
    modelo = info_modelos[mill_id]["modelo"]
    ubicacion = info_modelos[mill_id]["ubicacion"]

    # Construir el diccionario de datos para el molino
    data = {
        "mill_id": mill_id,
        "id": id,
        "model": modelo,
        "location": ubicacion,
        "timestamp": timestamp,
        "value": {
            "velocidad_viento": velocidad_viento,
            "direccion_viento": direccion_viento,
            "produccion_energia": produccion_energia,
            "temperatura_ambiente": temperatura_ambiente,
            "humedad": humedad,
            "presion_atmosferica": presion_atmosferica,
            "vibraciones": vibraciones
        }
    }
    return data

def generar_periodicamente():
    """
    Función para generar datos simulados periódicamente y enviarlos a la API.
    """
    global ESPERA
    t = threading.Timer(ESPERA, generar_periodicamente)
    t.start()
    
    global NUM_MOLINOS
    for i in range(NUM_MOLINOS):
        global p_error
        # Generar datos para cada molino y enviarlos a la API
        new_data = generate_windmill_data(i, p_error)
        url_post = "http://127.0.0.1:8000/datos-molinos/"
        post_response = requests.post(url_post, json=new_data)
        post_response.json()
    print("--------- Nuevos datos ------------")

# Configuración de parámetros
NUM_MOLINOS = 10  # Número de molinos a simular
ESPERA = 10  # Tiempo de espera entre cada iteración de generación de datos
p_error = 0.1  # Probabilidad de introducir errores en los datos

# Iniciar la generación periódica de datos
generar_periodicamente()
