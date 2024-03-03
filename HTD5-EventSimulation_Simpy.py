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
                # Pasa a IO o termina
                if self.instrucciones <= 0:
                    # Tiempo de fin
                    self.hora_fin = self.env.now
                    print(f"{self.env.now} [TERMINATED] {self.name} terminado.")
                    cpu.release(req)
                    break
                else:
                    random_num = random.randint(1, 2)
                    if random_num == 1:
                        # Espera en IO
                        print(f"{self.env.now} [WAITING] {self.name} -> Haciendo operaciones de I/O.")     
                    # Regresa a la cola de CPU esperando tiempo de llegada de proceso
                    yield env.timeout(round(random.expovariate(1/intervalo)), 1)
                    print(f"{self.env.now} [READY] {self.name} -> instrucciones pendientes {self.instrucciones}.")
                    yield req
        # Retorna la memoria utilizada.
        yield self.ram.put(self.memoria)

def crear_proceso(env, ram, cpu, num_procesos):
    for i in range(num_procesos):
        proceso = Proceso(f"Proceso {i}", env, ram, cpu)
        env.process(proceso.ejecutar())
        lista_procesos.append(proceso)
        
# Configuración de la simulación
env = simpy.Environment()
ram = simpy.Container(env, init=40, capacity=40)
cpu = simpy.Resource(env, capacity=1)

crear_proceso(env, ram, cpu, num_procesos)
env.run()


