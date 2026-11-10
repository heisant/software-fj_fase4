# ======================================================================================================================
# MÓDULO: servicios.py
# DESCRIPCIÓN: Clase abstracta Servicio y tres servicios especializados. 
#              Implementa polimorfismo y simulación de sobrecarga de métodos con *opciones.
# AUTOR: Heiner Santana Muñoz - Grupo 62 - UNAD
# ======================================================================================================================

from abc import abstractmethod
from .entidades import EntidadBase
from .excepciones import CalculoInconsistenteError, ServicioInvalidoError, ServicioNoDisponibleError

class Servicio(EntidadBase):
    """Servicio genérico de Software FJ."""
    _familia = "servicio"
    IVA = 0.19

    def __init__(self, nombre, tarifa_hora):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio requiere un nombre")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def deshabilitar(self):
        self._disponible = False

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"'{self._nombre}' no está disponible")

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def validar_parametros(self, horas):
        pass

    def calcular_costo_total(self, horas, *opciones):
        """Simulación de sobrecarga: (horas) | (horas, impuesto) | (horas, impuesto, descuento)."""
        if len(opciones) > 2:
            raise CalculoInconsistenteError("Demasiados parámetros para el cálculo")
        impuesto = opciones[0] if len(opciones) >= 1 else self.IVA
        descuento = opciones[1] if len(opciones) == 2 else 0.0
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise CalculoInconsistenteError("Impuesto o descuento fuera de rango (0 a 1)")
        base = self.calcular_costo(horas)
        total = base * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El total calculado es negativo")
        return round(total, 2)


class ReservaSala(Servicio):
    def __init__(self, nombre, tarifa_hora, capacidad):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:
            raise ServicioInvalidoError("Las salas se reservan de 1 a 8 horas")

    def calcular_costo(self, horas):
        self.validar_parametros(horas)
        recargo = 1.10 if self._capacidad > 20 else 1.0
        return self._tarifa_hora * horas * recargo

    def describir(self):
        return f"Sala '{self._nombre}' para {self._capacidad} personas, ${self._tarifa_hora:,.0f}/hora"


class AlquilerEquipo(Servicio):
    def __init__(self, nombre, tarifa_hora, unidades):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(unidades, int) or unidades <= 0:
            raise ServicioInvalidoError(f"Unidades inválidas: {unidades!r}")
        self._unidades = unidades

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError("Los equipos se alquilan de 1 a 72 horas")

    def calcular_costo(self, horas):
        self.validar_parametros(horas)
        descuento = 0.85 if horas >= 24 else 1.0
        return self._tarifa_hora * horas * descuento

    def describir(self):
        return f"Equipo '{self._nombre}' ({self._unidades} unidades), ${self._tarifa_hora:,.0f}/hora"


class AsesoriaEspecializada(Servicio):
    NIVELES = {"basico": 1.0, "avanzado": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, nivel):
        super().__init__(nombre, tarifa_hora)
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel de asesoría inválido: {nivel!r}")
        self._nivel = nivel

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 6:
            raise ServicioInvalidoError("Las asesorías duran entre 0.5 y 6 horas")

    def calcular_costo(self, horas):
        self.validar_parametros(horas)
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self):
        return f"Asesoría '{self._nombre}' nivel {self._nivel}, ${self._tarifa_hora:,.0f}/hora"
