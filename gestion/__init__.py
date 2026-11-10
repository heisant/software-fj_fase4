# ======================================================================================================================
# MÓDULO: __init__.py
# DESCRIPCIÓN: Archivo inicializador del paquete 'gestion'.
#              Exporta todas las clases principales para facilitar su uso en main.py.
# AUTOR: Heiner Santana Muñoz - Grupo 3 - UNAD
# ======================================================================================================================

# Importamos las clases y excepciones desde sus respectivos módulos
from .reserva import Reserva, ReservaInvalidaError, ServicioNoDisponibleError
from .cliente import Cliente, ClienteInvalidoError, Entidad
from .servicios import (Servicio, ReservaDeSala, AlquilerDeEquipo, 
                        AsesoriaEspecializada, TarifaInvalidaError, ParametroServicioError)

# Lista de clases públicas que se exportan al importar el paquete
__all__ = [
    # Entidades
    'Entidad', 'Cliente',
    # Servicios
    'Servicio', 'ReservaDeSala', 'AlquilerDeEquipo', 'AsesoriaEspecializada',
    # Reservas
    'Reserva',
    # Excepciones
    'ClienteInvalidoError', 'ServicioNoDisponibleError', 'ReservaInvalidaError',
    'TarifaInvalidaError', 'ParametroServicioError'
]
