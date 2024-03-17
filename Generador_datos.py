import json
import random
import datetime

# Definir modelos y ubicaciones constantes para cada molino
MODELOS = {
    "modelo_1": "G58",
    "modelo_2": "BS32",
    "modelo_3": "Modelo C"
}

UBICACIONES = {
    "ubicacion_1": "Biota",
    "ubicacion_2": "Lorbes",
    "ubicacion_3": "Merindad"
}

def generate_windmill_data(mill_id):
    """
    Función para generar datos simulados de un molino de viento.
    """
    timestamp = datetime.datetime.now().isoformat()
    wind_speed = round(random.uniform(0, 25), 2)  # Velocidad del viento en m/s
    power_output = round(random.uniform(0, 100), 2)  # Salida de energía en watts

    # Obtener modelo y ubicación para el molino
    modelo = MODELOS.get(mill_id, "Desconocido")
    ubicacion = UBICACIONES.get(mill_id, "Desconocido")

    data = {
        "mill_id": mill_id,
        "timestamp": timestamp,
        "wind_speed": wind_speed,
        "power_output": power_output,
        "model": modelo,
        "location": ubicacion
    }

    return data

def generate_multiple_windmill_data(num_mills):
    """
    Función para generar datos de múltiples molinos de viento.
    """
    mills_data = []
    for i in range(num_mills):
        mill_id = f"mill_{i + 1}"
        mill_data = generate_windmill_data(mill_id)
        mills_data.append(mill_data)

    return mills_data

def save_data_to_json(data, filename):
    """
    Función para guardar datos en un archivo JSON.
    """
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    num_mills = 10  # Número de molinos de viento
    mills_data = generate_multiple_windmill_data(num_mills)
    save_data_to_json(mills_data, "windmill_data.json")
