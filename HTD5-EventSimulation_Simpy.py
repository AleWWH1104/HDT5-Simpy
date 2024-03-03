import random
import simpy
import csv

# Parámetros de la simulación
intervalo = 10
num_procesos = 20
num_instrucciones = 3
random.seed(11)
lista_procesos = []

class Proceso:
    def __init__(self, name, env, ram, cpu):
        self.name = name
        self.env = env
        self.ram = ram
        self.cpu = cpu
        self.instrucciones = random.randint(1, 10)
        self.memoria = random.randint(1, 10)
        self.hora_inicio = None
        self.hora_fin = 0
