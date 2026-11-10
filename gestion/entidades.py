# ======================================================================================================================
# MÓDULO: entidades.py
# DESCRIPCIÓN: Clase abstracta que representa las entidades generales del sistema. 
#              Gestiona la asignación automática de IDs mediante contadores por familia.
# AUTOR: Heiner Santana Muñoz - Grupo 62 - UNAD
# ======================================================================================================================

from abc import ABC, abstractmethod

class EntidadBase(ABC):
    """Base común para Cliente, Servicio y Reserva."""
    _contadores = {}
    _familia = "entidad"

    def __init__(self):
        EntidadBase._contadores[self._familia] = EntidadBase._contadores.get(self._familia, 0) + 1
        self._id = EntidadBase._contadores[self._familia]

    @property
    def id(self):
        """Expone el id como propiedad de solo lectura (encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Obliga a las clases hijas a implementar una descripción en texto."""
        pass

    def __str__(self):
        """Representación en texto por defecto."""
        return self.describir()
