"""Clase abstracta que representa las entidades generales del sistema."""  # Docstring del módulo
from abc import ABC, abstractmethod  # Herramientas para clases abstractas


class EntidadBase(ABC):  # Clase abstracta: no se puede instanciar directamente
    """Base común para Cliente, Servicio y Reserva."""  # Descripción

    _contadores = {}  # Contadores por tipo de entidad (cliente, servicio, reserva)
    _familia = "entidad"  # Tipo de entidad; cada clase principal lo redefine

    def __init__(self):  # Constructor de la entidad
        EntidadBase._contadores[self._familia] = EntidadBase._contadores.get(self._familia, 0) + 1  # Suma 1 al contador del tipo
        self._id = EntidadBase._contadores[self._familia]  # Asigna el identificador (atributo protegido)

    @property  # Expone el id como propiedad de solo lectura (encapsulación)
    def id(self):  # Getter del identificador
        return self._id  # Devuelve el id

    @abstractmethod  # Obliga a las clases hijas a implementarlo
    def describir(self):  # Devuelve una descripción en texto de la entidad
        pass  # Sin implementación en la clase abstracta

    def __str__(self):  # Representación en texto por defecto
        return self.describir()  # Reutiliza el método polimórfico describir
