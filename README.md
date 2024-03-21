# Entrega-3-iot

- **Nombre**: Claudia Viñals Perlado
- **Repositorio**: [Entrega-3-iot](https://github.com/vipeclaudia103/Entrega-3-iot.git)
- **Presentación**: ["Reto 3"](https://prezi.com/view/RtBNlvanOcqsAG5OFsFc/)

# Explicación de los pasos seguidos

- Investigación sobre los detalles de los molinos eólicos y el funcionamiento de FastAPI.
- Generación de datos: El programa se encuentra en el archivo ['molinos.py'](molinos.py).

    1. Crear una función para generar datos de los molinos eólicos.
    2. Establecer una estructura para generar 10 molinos de manera consistente, siempre siendo los mismos 10 generadores de origen (similar a un caso de uso).
    3. Crear datos con una probabilidad de error específica.
    4. Utilizar hilos para la generación periódica de los datos.
    5. Envío de los datos generados a la API.

- Configuración de la API: La configuración de la API se encuentra en el archivo ['main.py'](main.py).
    1. Crear una estructura simple y verificar su actividad.
    2. Establecer una estructura de validación de datos.
    3. Enviar datos con el método POST desde molinos.py y almacenarlos.
    4. Utilizar los datos almacenados para cálculos y publicarlos con el método GET.

# Instrucciones de uso

Cómo utilizar el programa paso a paso:

1. Instalación de librerías: Esto instalará todas las dependencias necesarias del proyecto de FastAPI.
```bash
pip install -r requirements.txt
```

2. Ejecución del código:

    2.1. Primero ejecutar la API mediante los siguientes comandos:
    ```bash
    cd Entrega-3-iot
    export PATH="$PATH:/home/cvp/.local/bin"
    uvicorn main:molinos --reload    
    ```
    2.2. Ejecutar el código de generación de datos.
    ```bash
    python3 molinos.py
    ```

3. Visualizar en el navegador, dos opciones:
    3.1. Visualizar los endpoints por separado, las URLs para cada endpoint:
       A. [Media global de todos los molinos](http://127.0.0.1:8000/medias-global)

       B. Los siguientes endpoints necesitan completarse al final con un dato para devolver la consulta. A continuación, un resumen de las características posibles de los molinos; estos son los datos que se deben introducir. Completar el campo con la palabra clave entre llaves.
            a. **Modelos**: V164-9.5 MW, SG 14-222 DD, N149, G58.
                Media por modelo de los molinos: 'http://127.0.0.1:8000/media-modelo/{modelo}', este [enlace corresponde a G58](http://127.0.0.1:8000/media-modelo/G58) 
            b. **Ubicación**: Biota Zona Norte, Biota Zona Sur, Biota Zona Oeste, Biota Zona Este.
                Media por la ubicación de los molinos: 'http://127.0.0.1:8000/media-ubi/{ubicación}', este [enlace corresponde a Biota Zona Oeste](http://127.0.0.1:8000/media-ubi/Biota%20Zona%20Oeste) 
            c. **mill_id**: valores desde el 0 hasta el 9. 
                Media por mill_id de los molinos: 'http://127.0.0.1:8000/media-mill_id/{mill_id}', este [enlace corresponde al molino 9](http://127.0.0.1:8000/media-mill_id/9) 

    3.2. Visualizar todos los métodos por la interfaz de FastAPI: URL para la documentación [http://127.0.0.1:8000/docs#/]( http://127.0.0.1:8000/docs#/)

4. Validación de datos: Comprobar si los datos con error se muestran en la comprobación de la API. Para ello, visualizar la terminal de ejecución de la API y la ventana de ejecución de la generación de datos de los molinos. En ambas terminales se imprimen los mensajes de error donde se indica qué valor y qué molino han tenido ese error. Los valores con error no se añaden al array de datos, de esta forma se visualiza que, efectivamente, llegan los datos erróneos pero no se introducen.

# Posibles vías de mejora

A. Agregar seguridad mediante tokens utilizando la librería JWT.
B. En lugar de utilizar un array, utilizar una base de datos.
C. Ampliar las funcionalidades de análisis de datos, obteniendo otros valores estadísticos.

# Problemas / Retos encontrados

- Validación correcta de los datos pero resultados fuera de rango.
- Comprensión en la conexión entre las aplicaciones.

# Alternativas posibles

BlackSheep es un marco web asíncrono para crear aplicaciones web basadas en eventos con Python. Está inspirado en Flask, ASP.NET Core y el trabajo de Yury Selivanov.
Litesta:r es un marco ASGI potente, flexible, de alto rendimiento y obstinado.

# Bibliografía

«Conoce los tipos de sensores para monitorizar aerogeneradores». Accedido el 21 de marzo de 2024. [https://instrumentacionycontrol.es/tipos-de-sensores-para-monitorizar-aerogeneradores/](https://instrumentacionycontrol.es/tipos-de-sensores-para-monitorizar-aerogeneradores/).

«Security - First Steps - FastAPI». Accedido el 21 de marzo de 2024. [https://fastapi.tiangolo.com/tutorial/security/first-steps/](https://fastapi.tiangolo.com/tutorial/security/first-steps/).

«Seven Alternatives To FastAPI To Explore and Contribute To | Python | by Carlos Armando Marcano Vargas | Medium». Accedido el 21 de marzo de 2024. [https://medium.com/@carlosmarcano2704/seven-alternatives-to-fastapi-to-explore-and-contribute-python-47bcd394bf31](https://medium.com/@carlosmarcano2704/seven-alternatives-to-fastapi-to-explore-and-contribute-python-47bcd394bf31).