import random
import simpy
import csv

# Parámetros de la simulación
intervalo = 10
num_procesos = 200
num_instrucciones = 3
random.seed(44)
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
        self.hora_fin = None

    def ejecutar(self):
        print(f"{self.env.now} [NEW] {self.name}, RAM requerida -> {self.memoria}")
        # Solicita memoria
        yield self.ram.get(self.memoria)
        print(f"{self.env.now} [READY] {self.name} -> cant instrucciones {self.instrucciones}.")   
        while self.instrucciones > 0: 
            # Solicita CPU
            with self.cpu.request() as req:
                yield req
                if self.hora_inicio is None:
                    self.hora_inicio = self.env.now
                # Ejecuta sus instrucciones
                print(f"{self.env.now} [RUNNING] {self.name}, hasta {num_instrucciones} instrucciones.")
                # Espera unidad de tiempo procesador
                yield self.env.timeout(1)
                self.instrucciones -= num_instrucciones  # Reducir las instrucciones restantes
                # Pasa a IO o termina
                if self.instrucciones <= 0:
                    break
                else:
                    random_num = random.randint(1, 2)
                    if random_num == 1:
                        # Espera en IO
                        print(f"{self.env.now} [WAITING] {self.name} -> Haciendo operaciones de I/O.")     
                        yield env.timeout(round(random.expovariate(1.0/intervalo)),1)
                    else:
                        # Regresa a la cola de CPU esperando tiempo de llegada de proceso
                        print(f"{self.env.now} [READY] {self.name} -> instrucciones pendientes {self.instrucciones}.")
        # Retorna la memoria utilizada.
        self.ram.put(self.memoria)
        # Tiempo de fin
        self.hora_fin = self.env.now
        print(f"{self.env.now} [TERMINATED] {self.name} terminado.")
        #cpu.release(req)

def crear_proceso(env, ram, cpu, num_procesos):
    for i in range(num_procesos):
        proceso = Proceso(f"Proceso {i}", env, ram, cpu)
        lista_procesos.append(proceso)
        env.process(proceso.ejecutar())
                      
# Configuración de la simulación
env = simpy.Environment()
ram = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=1)

crear_proceso(env, ram, cpu, num_procesos)
env.run()

# Crear y escribir en un archivo CSV
nombre_archivo = 'procesos.csv'

with open(nombre_archivo, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Escribir encabezados
    writer.writerow([f'{num_procesos}',f'Proceso #{num_procesos}', 'Hora de inicio', 'Hora de fin', 'Duración'])

    # Iterar sobre los procesos y escribir los datos
    for proceso in lista_procesos:
        duracion = proceso.hora_fin - proceso.hora_inicio
        writer.writerow([num_procesos, proceso.name, proceso.hora_inicio, proceso.hora_fin, duracion])

print(f"Los datos se han exportado en '{nombre_archivo}'")



