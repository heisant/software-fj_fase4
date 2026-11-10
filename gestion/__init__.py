# ======================================================================================================================
# MÓDULO: __init__.py
# DESCRIPCIÓN: Archivo inicializador del paquete 'gestion'. Permite importar las clases y funciones 
#              desde los submódulos de forma limpia y organizada.
# AUTOR: Heiner Santana Muñoz - Grupo 62 - UNAD
# ======================================================================================================================

from .excepciones import (
    ErrorSoftwareFJ, ClienteInvalidoError, ServicioInvalidoError,
    ServicioNoDisponibleError, CalculoInconsistenteError, ReservaError, OperacionNoPermitidaError
)
from .logger import registrar_evento, registrar_advertencia, registrar_error
from .entidades import EntidadBase
from .cliente import Cliente
from .servicios import Servicio, ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from .reserva import Reserva

__all__ = [
    'ErrorSoftwareFJ', 'ClienteInvalidoError', 'ServicioInvalidoError',
    'ServicioNoDisponibleError', 'CalculoInconsistenteError', 'ReservaError', 'OperacionNoPermitidaError',
    'registrar_evento', 'registrar_advertencia', 'registrar_error',
    'EntidadBase', 'Cliente', 'Servicio', 'ReservaSala', 'AlquilerEquipo', 'AsesoriaEspecializada', 'Reserva'
]
