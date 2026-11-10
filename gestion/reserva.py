# ======================================================================================================================
# MÓDULO: reserva.py
# DESCRIPCIÓN: Clase Reserva que integra cliente, servicio, duración y estado.
#              Implementa confirmación, cancelación y procesamiento con manejo de excepciones.
# AUTOR: Heiner Santana Muñoz - Grupo 3
# ======================================================================================================================

import logging
from datetime import datetime


# ======================================================================================================================
# EXCEPCIONES PERSONALIZADAS PARA RESERVAS
# ======================================================================================================================

class ReservaInvalidaError(Exception):
    """
    Excepción personalizada lanzada cuando hay un error al crear, 
    confirmar o cancelar una reserva.
    """
    pass


class ServicioNoDisponibleError(Exception):
    """
    Excepción personalizada lanzada cuando un servicio no está disponible
    para ser reservado.
    """
    pass


# ======================================================================================================================
# CLASE RESERVA
# ======================================================================================================================

class Reserva:
    """
    Clase que gestiona la reserva de un servicio por parte de un cliente.
    Integra: cliente, servicio, duración y estado de la reserva.
    """
    
    def __init__(self, id_reserva: int, cliente, servicio, duracion: int):
        """
        Constructor de la clase Reserva.
        
        Args:
            id_reserva (int): Identificador único de la reserva
            cliente: Objeto de tipo Cliente
            servicio: Objeto de tipo Servicio
            duracion (int): Duración de la reserva (horas, días o sesiones según el servicio)
        """
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"  # Estados posibles: Pendiente, Confirmada, Cancelada
        self.fecha_creacion = datetime.now()
        
        # Registrar en logs la creación de la reserva
        logging.info(f"Reserva {self.id_reserva} creada para {self.cliente.nombre} - Servicio: {self.servicio.nombre}")

    def confirmar(self):
        """
        Confirma la reserva aplicando validaciones y manejo de excepciones.
        Verifica disponibilidad del servicio y validez de la duración.
        """
        try:
            # Validación 1: Verificar que el servicio esté disponible
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre}' no está disponible para reserva."
                )
            
            # Validación 2: Verificar que la duración sea válida
            if self.duracion <= 0:
                raise ValueError("La duración de la reserva debe ser mayor a cero.")
            
            # Si todo está correcto, cambiar el estado a Confirmada
            self.estado = "Confirmada"
            logging.info(f"Reserva {self.id_reserva} CONFIRMADA exitosamente para {self.cliente.nombre}.")
            
        except ValueError as ve:
            # Encadenamiento de excepciones: capturamos ValueError y lanzamos ReservaInvalidaError
            logging.error(f"Error de validación en reserva {self.id_reserva}: {ve}")
            raise ReservaInvalidaError(
                f"Error de datos en la reserva {self.id_reserva}. Duración inválida."
            ) from ve
            
        except ServicioNoDisponibleError as sne:
            # Capturamos la excepción de servicio no disponible y la registramos
            logging.error(f"Error de disponibilidad en reserva {self.id_reserva}: {sne}")
            raise
            
        except Exception as e:
            # Captura genérica para cualquier otro error inesperado
            logging.error(f"Error inesperado al confirmar reserva {self.id_reserva}: {e}")
            raise ReservaInvalidaError(f"Error inesperado en la reserva {self.id_reserva}.") from e

    def cancelar(self):
        """
        Cancela la reserva si está en estado válido para cancelación.
        Lanza excepción si la reserva ya está cancelada.
        """
        try:
            # Validación: No se puede cancelar una reserva ya cancelada
            if self.estado == "Cancelada":
                raise ReservaInvalidaError(
                    f"La reserva {self.id_reserva} ya está cancelada. No se puede cancelar nuevamente."
                )
            
            # Cambiar el estado a Cancelada
            self.estado = "Cancelada"
            logging.info(f"Reserva {self.id_reserva} CANCELADA por {self.cliente.nombre}.")
            
        except ReservaInvalidaError as rie:
            # Re-lanzamos la excepción para que el llamador la maneje
            logging.error(f"Error al cancelar reserva {self.id_reserva}: {rie}")
            raise
            
        except Exception as e:
            # Captura genérica
            logging.error(f"Error inesperado al cancelar reserva {self.id_reserva}: {e}")
            raise ReservaInvalidaError(f"Error inesperado al cancelar reserva {self.id_reserva}.") from e

    def procesar(self):
        """
        Procesa la reserva calculando el costo total.
        Usa try/except/else/finally para demostrar control completo de flujo.
        
        Returns:
            float: Costo total de la reserva, o None si hubo error
        """
        try:
            # Intentamos calcular el costo usando el método polimórfico del servicio
            costo = self.servicio.calcular_costo(self.duracion)
            
        except Exception as e:
            # Si falla el cálculo, registramos el error
            logging.error(f"Error procesando reserva {self.id_reserva}: {e}")
            return None
            
        else:
            # Este bloque se ejecuta SOLO si no hubo excepciones en el try
            logging.info(f"Reserva {self.id_reserva} procesada exitosamente. Costo total: ${costo}")
            return costo
            
        finally:
            # Este bloque se ejecuta SIEMPRE, haya habido error o no
            logging.info(f"Finalizó el procesamiento de la reserva {self.id_reserva}. Estado final: {self.estado}")

    def __str__(self):
        """
        Método especial que retorna una representación en string de la reserva.
        """
        return (f"Reserva ID: {self.id_reserva} | "
                f"Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | "
                f"Duración: {self.duracion} | "
                f"Estado: {self.estado} | "
                f"Fecha: {self.fecha_creacion.strftime('%Y-%m-%d %H:%M')}")
