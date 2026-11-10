
from .excepciones import (
    ClienteNoValidoError,
    ServicioNoValidoError,
    DuracionInvalidaError,
    EstadoReservaError,
    CalculoCostoError
)


class Reserva:
    """
    Representa una reserva de un servicio de Software FJ.
    """

    def __init__(self, id_reserva, cliente, servicio, duracion):

        # Validar los datos recibidos
        if cliente is None:
            raise ClienteNoValidoError("El cliente es obligatorio.")

        if servicio is None:
            raise ServicioNoValidoError("El servicio es obligatorio.")

        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise DuracionInvalidaError(
                "La duración debe ser un número positivo."
            )

        # Atributos encapsulados
        self.__id_reserva = id_reserva
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"

    def confirmar(self):
        """Confirma una reserva pendiente."""

        if self.__estado != "Pendiente":
            raise EstadoReservaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.__estado = "Confirmada"
        return "Reserva confirmada correctamente."

    def cancelar(self):
        """Cancela una reserva que no esté cancelada."""

        if self.__estado == "Cancelada":
            raise EstadoReservaError("La reserva ya está cancelada.")

        self.__estado = "Cancelada"
        return "Reserva cancelada correctamente."

    def procesar(self):
        """Calcula el costo de una reserva confirmada."""

        if self.__estado != "Confirmada":
            raise EstadoReservaError(
                "La reserva debe estar confirmada."
            )

        try:
            return self.__servicio.calcular_costo(self.__duracion)

        except Exception as error:
            raise CalculoCostoError(
                "No fue posible calcular el costo de la reserva."
            ) from error

    def mostrar_informacion(self):
        """Muestra los datos principales de la reserva."""

        print("ID de reserva:", self.__id_reserva)
        print("Cliente:", self.__cliente)
        print("Servicio:", self.__servicio)
        print("Duración:", self.__duracion)
        print("Estado:", self.__estado)
