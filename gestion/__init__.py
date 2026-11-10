# ======================================================================================================================
# MÓDULO: __init__.py
# DESCRIPCIÓN: Archivo inicializador del paquete 'gestion'.
#              Permite que Python reconozca la carpeta 'gestion' como un módulo importable.
#              Desde aquí se exportan las clases principales para facilitar su uso en main.py.
# AUTOR: Heiner Santana Muñoz - Grupo 3 - UNAD
# ======================================================================================================================

# Importamos las clases principales desde sus respectivos módulos
# Esto permite que en main.py se pueda hacer: from gestion import Cliente, Reserva, etc.

from .reserva import Reserva, ReservaInvalidaError, ServicioNoDisponibleError
# from .cliente import Cliente, ClienteInvalidoError  # Se descomentará cuando se cree cliente.py
# from .servicios import Servicio, ReservaDeSala, AlquilerDeEquipo, AsesoriaEspecializada  # Se descomentará cuando se cree servicios.py

# Lista de clases públicas que se exportan al importar el paquete
__all__ = [
    'Reserva',
    'ReservaInvalidaError',
    'ServicioNoDisponibleError',
    # 'Cliente', 'ClienteInvalidoError',
    # 'Servicio', 'ReservaDeSala', 'AlquilerDeEquipo', 'AsesoriaEspecializada'
]
