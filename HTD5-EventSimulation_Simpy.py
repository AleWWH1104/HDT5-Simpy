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

    def ejecutar(self):
        print(f"{self.env.now} [NEW] {self.name}, RAM requerida -> {self.memoria}")
        # Solicita memoria
        yield self.ram.get(self.memoria)
        print(f"{self.env.now} [READY] {self.name} -> cant instrucciones {self.instrucciones}.")   
        while self.instrucciones > 0: 
            # Solicita CPU
            with self.cpu.request() as req:
                if self.hora_inicio == None:
                    self.hora_inicio = self.env.now
                yield req
                # Ejecuta sus instrucciones
                print(f"{self.env.now} [RUNNING] {self.name}, ejecutando hasta {num_instrucciones} instrucciones.")
                # Espera unidad de tiempo procesador
                yield self.env.timeout(1)
                self.instrucciones -= num_instrucciones  # Reducir las instrucciones restantes
        

# Configuración de la simulación
env = simpy.Environment()
ram = simpy.Container(env, init=40, capacity=40)
cpu = simpy.Resource(env, capacity=1)



