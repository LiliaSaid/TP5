"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

# 1. Definición de mecanismos de sincronización
mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)


def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))
        
        # Sincronización del acceso al tarro de miel:
        sem_tarro_disponible.acquire()
        
        with mutex:
            if not simulacion_activa:
                sem_tarro_disponible.release()
                break
                
            if tarro_miel < M:
                tarro_miel += 1
                print(f"🐝 Abeja {id_abeja} depositó miel. Porciones en el tarro: {tarro_miel}/{M}")
                
                if tarro_miel == M:
                    print(f"🍯 ¡El tarro está lleno! Abeja {id_abeja} despierta al oso 🐻")
                    sem_oso.release()  # Despierta al oso dormido
                else:
                    sem_tarro_disponible.release()  # Permite que otra abeja produzca
            else:
                sem_tarro_disponible.release()


def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros and simulacion_activa:
        # 1. Espera pasiva (bloqueado) hasta que la última abeja avise
        sem_oso.acquire()
        
        if not simulacion_activa:
            break

        # 2 y 3. Exclusión mutua para comerse toda la miel
        with mutex:
            print(f"🐻 El oso se despierta y se come los {tarro_miel} porciones de miel...")
            tarro_miel = 0
            tarros_comidos += 1
            print(f"🍽️ El oso comió {tarros_comidos}/{max_tarros} tarros y vuelve a dormir.")

        # 4. Habilita a las abejas a seguir produciendo
        sem_tarro_disponible.release()
        
    simulacion_activa = False


if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)

    # Crear hilos para el oso y las abejas
    hilo_oso = threading.Thread(target=oso, args=(2,))
    hilos_abejas = [
        threading.Thread(target=abeja, args=(i+1,), daemon=True) 
        for i in range(NUM_ABEJAS)
    ]

    # Iniciar hilos
    hilo_oso.start()
    for h in hilos_abejas:
        h.start()

    # Esperar a que el oso termine de comer
    hilo_oso.join()
    print("\n" + "=" * 60)
    print(" Simulación finalizada con éxito.")
    print("=" * 60)