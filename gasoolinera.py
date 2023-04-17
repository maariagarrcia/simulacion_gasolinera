
from multiprocessing import Process, Queue
from colorama import Fore
import time
import random

## EN LA GASOLINERA
# ===========================
# · Se crean el productor y el consumidor.
# · El productor produce gasolin ---> hechar entre 5 y 10 s  de gasolina
# · El consumidor consume gasolina.
# · Se limita el tamaño del tanque a 5 litros.
# · Si el tanque esta lleno el productor para.
# · Si el tanque esta vacio el consumidor espera.
# · Dps del consumo hay un retardo aleatorio ya que tiene q ir a pagar

# Parámetros de la simulación
# ===========================
# 50 coches
# 4 surtidores
#


def arrancar_todo(procesos) -> None:
    print("* Arrancando procesos...")
    for p in procesos:
        p.start()


def poner_gasolina(id_coche :int, nombre_combustible: str, cola: Queue) -> None:
    # Contador de coches con gasolina
    num_coches_gasolina = 0

    while True:
        # Cocinar -> Simular tiempo cocinado entre 5 y 10 
        time.sleep(random.randint(5,10))

        # Si no está llena la cola dejar plato
        # Si la cola esta llena se espera a que algun cliente
        # consuma algún plato.
        # Si timeout se supera el cocinero se va a su casa ya
        # que los clientes han dejado de comer

        try:
            cola.put([id_coche, num_coches_gasolina, nombre_combustible],
                     block=True, timeout=1)
            num_coches_gasolina += 1
            print(Fore.YELLOW+"+ Coche"+Fore.WHITE, id_coche, "con", nombre_combustible)
        except:
            print(Fore.RED+"+ Surtidor", id_coche,
                  "esta  vacio---> noo hay  coches", num_coches_gasolina, "<----------"+Fore.WHITE)
            return

        # se  van a la cola a pagar

       


def comer(id_coche, colas: list) -> None:
    # Decidir que tipode combustible quiere
    max_combustible = 2

    for x in range(1, max_combustible+1):
        # Seleccionar  combustible
        combustible: Queue = random.choice(colas)

        try:
            surtidor = combustible.get(block=True, timeout=3)

            # Comer -> Simular tiempo consumición plato
            time.sleep(random.randint(1))
            print(Fore.GREEN+"- Coche"+Fore.WHITE, id_coche, "surtidor", surtidor)

        except:
            # Se ha superado el tiempo máximo de espera de un
            # plato por parte del cliente que decide abandonar
            # el restaurante enfadado :-0
            print(Fore.RED+"- Coche:", id_coche,
                  "Me voy!!!. Son muuy lentos :-(", x-1,"<-----------"+Fore.WHITE)
            return 

    print(Fore.RED+"- Coche", id_coche, "suficiente tiempo esperando", x, "<-----------"+Fore.WHITE)


def crear_coches(cantidad, cola_combustible, cola_diesel) -> list():
    print("* Creando coches...")
    coches = []
    nombres_combustible = ["combustible", "diesel"]
    colas_comida = [cola_combustible, cola_diesel]

    for id_coches in range(0, cantidad):
        # Seleccionar que comida elabora el cocinero
        nombre_comida = nombres_combustible[id_coches % 2]
        cola_comida = colas_comida[id_coches % 2]

        coches.append(
            Process(target=poner_gasolina, args=[id_coches, nombre_comida, cola_comida]))

    return coches


def crear_combustible(cantidad, cola_gasolina, cola_diesel) -> list():
    coches = []

    print("* Creando comensales...")
    for id_coches in range(0, cantidad):
        coches.append(
            Process(target=comer, args=[id_coches, [cola_gasolina, cola_diesel]]))

    return coches


def esperar_finalizacion_procesos(procesos):
    print("* Esperando finalización procesos...")
    print("·")
    for p in procesos:
        p.join()


def main() -> None:
    print()
    print("Simulacion de Productor/Consumidor: Restaurante")
    print("· Se crean 4  surtidores que cada uno tiene una cola de 5 coches como max y  cada surtidor tiene un tipo de combustible ")
    print("· Se crean 50 coches")
    print("· Se limita el tamaño de las colas de coches en los surtidores")
    print("· Si las colas estan llenas no llegan mas  coches")
    print("· Si las colas estan vacias los llegan coches")
    print("·")

    # Crear colas (una por comida) capacidad máxima para 5 elementos
    max_gasolina = 2
    cola_gasolina = Queue(max_gasolina)
    max_diesel=2
    cola_diesel = Queue(max_diesel)

    # Crear procesos
    procesos = []
    procesos = crear_coches(4, cola_gasolina, cola_diesel)
    procesos = procesos + crear_combustible(50, cola_gasolina, cola_diesel)

    # Ejecutar procesos consumidores y productores (comensales y cocineros)
    arrancar_todo(procesos)

    esperar_finalizacion_procesos(procesos)

    print("*** Simulación finalizada ***")


if __name__ == '__main__':
    main()

