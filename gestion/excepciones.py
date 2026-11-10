"""Excepciones personalizadas del sistema Software FJ."""  # Docstring del módulo


class ErrorSoftwareFJ(Exception):  # Excepción base de la que heredan todas las demás
    """Error general del sistema Software FJ."""  # Descripción de la clase

    def __init__(self, mensaje, codigo="FJ-000"):  # Constructor con mensaje y código de error
        super().__init__(mensaje)  # Llama al constructor de Exception con el mensaje
        self.codigo = codigo  # Guarda el código para identificar el tipo de falla en el log


class ClienteInvalidoError(ErrorSoftwareFJ):  # Error al validar datos de un cliente
    def __init__(self, mensaje):  # Constructor propio
        super().__init__(mensaje, "FJ-101")  # Código asignado a errores de cliente


class ServicioInvalidoError(ErrorSoftwareFJ):  # Error al crear o validar un servicio
    def __init__(self, mensaje):  # Constructor propio
        super().__init__(mensaje, "FJ-201")  # Código asignado a errores de servicio


class ServicioNoDisponibleError(ErrorSoftwareFJ):  # Error cuando el servicio no se puede usar
    def __init__(self, mensaje):  # Constructor propio
        super().__init__(mensaje, "FJ-202")  # Código para servicio no disponible


class CalculoInconsistenteError(ErrorSoftwareFJ):  # Error en cálculos de costos
    def __init__(self, mensaje):  # Constructor propio
        super().__init__(mensaje, "FJ-301")  # Código para cálculos inconsistentes


class ReservaError(ErrorSoftwareFJ):  # Error en el flujo de una reserva
    def __init__(self, mensaje):  # Constructor propio
        super().__init__(mensaje, "FJ-401")  # Código para errores de reserva


class OperacionNoPermitidaError(ErrorSoftwareFJ):  # Error por una acción no válida según el estado
    def __init__(self, mensaje):  # Constructor propio
        super().__init__(mensaje, "FJ-402")  # Código para operaciones no permitidas
