 # ======================================================================================================================
# MÓDULO: reserva.py
# DESCRIPCIÓN: Clase Reserva que integra cliente, servicio, duración y estado. 
#              Implementa confirmación, cancelación y procesamiento con manejo avanzado de excepciones.
# AUTOR: Heiner Santana Muñoz - Grupo 3 - UNAD
# ======================================================================================================================

from .entidades import EntidadBase
from .excepciones import ErrorSoftwareFJ, OperacionNoPermitidaError, ReservaError
from . import logger

class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""
    _familia = "reserva"
    PENDIENTE, CONFIRMADA, CANCELADA, FALLIDA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "FALLIDA"

    def __init__(self, cliente, servicio, horas):
        super().__init__()
        if cliente is None or servicio is None:
            raise ReservaError("La reserva requiere cliente y servicio")
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = self.PENDIENTE
        self._total = None

    @property
    def estado(self):
        return self._estado

    @property
    def total(self):
        return self._total

    def procesar(self):
        try:
            self._servicio.verificar_disponibilidad()
            self._total = self._servicio.calcular_costo_total(self._horas)
        except ErrorSoftwareFJ as error:
            self._estado = self.FALLIDA
            raise ReservaError(f"No se pudo procesar la reserva #{self.id}") from error
        else:
            logger.registrar_evento(f"Reserva #{self.id} procesada, total ${self._total:,.2f}")
        finally:
            logger.registrar_evento(f"Reserva #{self.id} terminó el procesamiento con estado {self._estado}")

    def confirmar(self):
        if self._estado != self.PENDIENTE or self._total is None:
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self._estado}")
        self._estado = self.CONFIRMADA
        logger.registrar_evento(f"Reserva #{self.id} confirmada")

    def cancelar(self):
        if self._estado in (self.CANCELADA, self.FALLIDA):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self._estado}")
        self._estado = self.CANCELADA
        logger.registrar_evento(f"Reserva #{self.id} cancelada")

    def describir(self):
        total = f"${self._total:,.2f}" if self._total is not None else "sin calcular"
        return f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | {self._horas} h | {self._estado} | {total}"
