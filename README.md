# Simulación de Procesos usando SIMPY

Este programa simula el procesamiento de múltiples procesos en un entorno computacional utilizando la biblioteca SimPy en Python. Permite explorar y analizar el comportamiento de los procesos, la asignación de recursos y los tiempos de ejecución en un sistema simulado.

## Descripción del Programa

El programa consta de varios componentes principales:

- **Clase Proceso:** Define los atributos y comportamientos de un proceso, incluyendo la asignación de memoria, la solicitud y liberación de recursos de la CPU, y la ejecución de instrucciones.

- **Función crear_proceso:** Genera una serie de procesos con parámetros aleatorios y los introduce en el entorno de simulación.

- **Entorno de Simulación (SimPy):** Crea y gestiona el paso del tiempo y la interacción entre los diferentes procesos, incluyendo la ejecución de instrucciones y las operaciones de entrada/salida.

## Instrucciones de Uso
1. **Personalización de Parámetros:**

   Puedes ajustar los parámetros de la simulación, como el número de procesos, intervalos de llegada, capacidad de la memoria y la CPU, modificando las variables en el archivo.

2. **Análisis de Resultados:**

   El programa generará un archivo CSV llamado `procesos.csv` que contiene los detalles de cada proceso, incluyendo su hora de inicio, hora de finalización y duración. Utiliza estos datos para realizar un análisis del rendimiento y comportamiento de los procesos simulados.