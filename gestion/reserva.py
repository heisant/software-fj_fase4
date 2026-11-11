"""Clase Reserva: integra cliente, servicio, duración y estado."""  # Docstring del módulo
from .entidades import EntidadBase  # Clase abstracta base
from .excepciones import (  # Excepciones propias usadas aquí
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ReservaError,
)
from . import logger  # Módulo de registro de eventos y errores (mismo paquete)


class Reserva(EntidadBase):  # La reserva es una entidad del sistema
    """Reserva de un servicio por parte de un cliente."""  # Descripción

    _familia = "reserva"  # Tipo de entidad para el contador de ids
    PENDIENTE, CONFIRMADA, CANCELADA, FALLIDA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "FALLIDA"  # Estados

    def __init__(self, cliente, servicio, horas):  # Constructor de la reserva
        super().__init__()  # Genera el id
        if cliente is None or servicio is None:  # Faltan parámetros obligatorios
            raise ReservaError("La reserva requiere cliente y servicio")  # Error propio
        self._cliente = cliente  # Guarda el cliente
        self._servicio = servicio  # Guarda el servicio
        self._horas = horas  # Guarda la duración solicitada
        self._estado = self.PENDIENTE  # Toda reserva inicia pendiente
        self._total = None  # El total se calcula al procesar

    @property  # Getter del estado
    def estado(self):  # Devuelve el estado actual
        return self._estado  # Valor protegido

    @property  # Getter del total
    def total(self):  # Devuelve el total calculado
        return self._total  # Valor protegido

    def procesar(self):  # Valida la reserva y calcula su costo
        try:  # Bloque principal con try/except/else/finally
            self._servicio.verificar_disponibilidad()  # Comprueba que el servicio esté disponible
            self._total = self._servicio.calcular_costo_total(self._horas)  # Calcula el costo con IVA
        except ErrorSoftwareFJ as error:  # Captura cualquier error propio del sistema
            self._estado = self.FALLIDA  # La reserva queda fallida
            raise ReservaError(f"No se pudo procesar la reserva #{self.id}") from error  # Encadena la causa
        else:  # Se ejecuta solo si no hubo errores
            logger.registrar_evento(f"Reserva #{self.id} procesada, total ${self._total:,.2f}")  # Registra éxito
        finally:  # Se ejecuta siempre
            logger.registrar_evento(f"Reserva #{self.id} terminó el procesamiento con estado {self._estado}")  # Cierre

    def confirmar(self):  # Confirma una reserva pendiente
        if self._estado != self.PENDIENTE or self._total is None:  # Solo pendientes ya procesadas
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self._estado}")  # Error propio
        self._estado = self.CONFIRMADA  # Cambia el estado
        logger.registrar_evento(f"Reserva #{self.id} confirmada")  # Registra el evento

    def cancelar(self):  # Cancela una reserva
        if self._estado in (self.CANCELADA, self.FALLIDA):  # No se cancela lo ya cancelado o fallido
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self._estado}")  # Error propio
        self._estado = self.CANCELADA  # Cambia el estado
        logger.registrar_evento(f"Reserva #{self.id} cancelada")  # Registra el evento

    def describir(self):  # Implementa el método abstracto
        total = f"${self._total:,.2f}" if self._total is not None else "sin calcular"  # Texto del total
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "  # Primera parte
                f"{self._horas} h | {self._estado} | {total}")  # Segunda parte
