
class ErrorSoftwareFJ(Exception):
    """Excepcion general del sistema Software FJ."""
    pass


class ClienteNoValidoError(ErrorSoftwareFJ):
    """Se genera cuando los datos del cliente no son validos."""
    pass


class ServicioNoValidoError(ErrorSoftwareFJ):
    """Se genera cuando el servicio no es valido."""
    pass


class DuracionInvalidaError(ErrorSoftwareFJ):
    """Se genera cuando la duracion de la reserva es incorrecta."""
    pass


class EstadoReservaError(ErrorSoftwareFJ):
    """Se genera cuando una operacion no esta permitida por el estado de la reserva."""
    pass


class CalculoCostoError(ErrorSoftwareFJ):
    """Se genera cuando ocurre un error al calcular el costo del servicio."""
    pass
