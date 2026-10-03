

"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 1: Sincronización Básica y Trazas de Señalización
"""

import sys
import threading
import time

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================================================
# PARTE 1: Exclusión Mutua y Ordenamiento sobre Variable Compartida
# ============================================================================

X = 199

# Semáforo de orden: A debe avisarle a B cuando termine
sem_orden_AB = threading.Semaphore(0)

def proceso_A():
    global X
    X = X + 1  # 199 + 1 = 200
    print(f"[Parte 1] Proceso A: X = {X}")
    sem_orden_AB.release()  # Despierta a B

def proceso_B():
    global X
    sem_orden_AB.acquire()  # Espera a que A termine
    X = X // 10  # 200 // 10 = 20
    print(f"[Parte 1] Proceso B: X = {X}")


# ============================================================================
# PARTE 2: Sincronización de Trazas Estrictas (Secuencia ABCABC)
# ============================================================================

# A arranca habilitado en 1; B y C esperan en 0
sem_sig_A = threading.Semaphore(1)
sem_sig_B = threading.Semaphore(0)
sem_sig_C = threading.Semaphore(0)

def proceso_emisor_A(rondas=3):
    for i in range(rondas):
        sem_sig_A.acquire()
        print(f"[Parte 2] Ronda {i+1} -> 🅰️ Proceso A ejecutando")
        time.sleep(0.1)
        sem_sig_B.release()

def proceso_receptor_B(rondas=3):
    for i in range(rondas):
        sem_sig_B.acquire()
        print(f"[Parte 2] Ronda {i+1} -> 🅱️ Proceso B ejecutando")
        time.sleep(0.1)
        sem_sig_C.release()

def proceso_receptor_C(rondas=3):
    for i in range(rondas):
        sem_sig_C.acquire()
        print(f"[Parte 2] Ronda {i+1} -> 🅲 Proceso C ejecutando")
        time.sleep(0.1)
        sem_sig_A.release()


if __name__ == "__main__":
    print("=" * 60)
    print("EJERCICIO 1 - PARTE 1: Variable Compartida")
    print("=" * 60)
    hA = threading.Thread(target=proceso_A)
    hB = threading.Thread(target=proceso_B)
    hA.start(); hB.start()
    hA.join(); hB.join()

    print("\n" + "=" * 60)
    print("EJERCICIO 1 - PARTE 2: Secuencia Estricta ABCABC")
    print("=" * 60)
    tA = threading.Thread(target=proceso_emisor_A)
    tB = threading.Thread(target=proceso_receptor_B)
    tC = threading.Thread(target=proceso_receptor_C)
    tA.start(); tB.start(); tC.start()
    tA.join(); tB.join(); tC.join()