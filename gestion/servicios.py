"""Servicio abstracto y tres servicios especializados (polimorfismo)."""  # Docstring del módulo
from abc import abstractmethod  # Para declarar métodos abstractos

from .entidades import EntidadBase  # Clase abstracta base
from .excepciones import (  # Excepciones propias usadas aquí
    CalculoInconsistenteError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)


class Servicio(EntidadBase):  # Clase abstracta de todos los servicios
    """Servicio genérico de Software FJ."""  # Descripción

    _familia = "servicio"  # Tipo de entidad para el contador de ids
    IVA = 0.19  # Impuesto por defecto (19 %)

    def __init__(self, nombre, tarifa_hora):  # Constructor común
        super().__init__()  # Genera el id
        if not isinstance(nombre, str) or not nombre.strip():  # El nombre debe ser texto no vacío
            raise ServicioInvalidoError("El servicio requiere un nombre")  # Lanza error propio
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:  # La tarifa debe ser positiva
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}")  # Lanza error propio
        self._nombre = nombre.strip()  # Guarda el nombre (protegido)
        self._tarifa_hora = float(tarifa_hora)  # Guarda la tarifa por hora
        self._disponible = True  # Todo servicio nace disponible

    @property  # Getter del nombre
    def nombre(self):  # Devuelve el nombre
        return self._nombre  # Valor protegido

    @property  # Getter de la disponibilidad
    def disponible(self):  # Devuelve si se puede reservar
        return self._disponible  # Valor protegido

    def deshabilitar(self):  # Marca el servicio como no disponible
        self._disponible = False  # Cambia el estado

    def verificar_disponibilidad(self):  # Lanza error si no está disponible
        if not self._disponible:  # Si está deshabilitado
            raise ServicioNoDisponibleError(f"'{self._nombre}' no está disponible")  # Error propio

    @abstractmethod  # Cada servicio calcula su costo base a su manera
    def calcular_costo(self, horas):  # Costo antes de impuestos y descuentos
        pass  # Sin implementación aquí

    @abstractmethod  # Cada servicio valida sus propios parámetros
    def validar_parametros(self, horas):  # Valida la duración solicitada
        pass  # Sin implementación aquí

    def calcular_costo_total(self, horas, *opciones):  # Método sobrecargado (simulado con *opciones)
        """Variantes: (horas) | (horas, impuesto) | (horas, impuesto, descuento)."""  # Variantes aceptadas
        if len(opciones) > 2:  # Máximo dos parámetros opcionales
            raise CalculoInconsistenteError("Demasiados parámetros para el cálculo")  # Error propio
        impuesto = opciones[0] if len(opciones) >= 1 else self.IVA  # Impuesto opcional, por defecto IVA
        descuento = opciones[1] if len(opciones) == 2 else 0.0  # Descuento opcional, por defecto cero
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:  # Ambos deben ser proporciones
            raise CalculoInconsistenteError("Impuesto o descuento fuera de rango (0 a 1)")  # Error propio
        base = self.calcular_costo(horas)  # Costo base polimórfico
        total = base * (1 - descuento) * (1 + impuesto)  # Aplica descuento y luego impuesto
        if total < 0:  # Un total negativo es inconsistente
            raise CalculoInconsistenteError("El total calculado es negativo")  # Error propio
        return round(total, 2)  # Devuelve el total redondeado


class ReservaSala(Servicio):  # Servicio 1: reserva de salas
    def __init__(self, nombre, tarifa_hora, capacidad):  # Constructor con capacidad
        super().__init__(nombre, tarifa_hora)  # Datos comunes
        if not isinstance(capacidad, int) or capacidad <= 0:  # La capacidad debe ser entero positivo
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")  # Error propio
        self._capacidad = capacidad  # Guarda la capacidad de personas

    def validar_parametros(self, horas):  # Sobrescribe la validación
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:  # Salas: de 1 a 8 horas
            raise ServicioInvalidoError("Las salas se reservan de 1 a 8 horas")  # Error propio

    def calcular_costo(self, horas):  # Sobrescribe el costo
        self.validar_parametros(horas)  # Valida antes de calcular
        recargo = 1.10 if self._capacidad > 20 else 1.0  # Recargo del 10 % para salas grandes
        return self._tarifa_hora * horas * recargo  # Costo base de la sala

    def describir(self):  # Sobrescribe la descripción
        return f"Sala '{self._nombre}' para {self._capacidad} personas, ${self._tarifa_hora:,.0f}/hora"  # Texto


class AlquilerEquipo(Servicio):  # Servicio 2: alquiler de equipos
    def __init__(self, nombre, tarifa_hora, unidades):  # Constructor con unidades
        super().__init__(nombre, tarifa_hora)  # Datos comunes
        if not isinstance(unidades, int) or unidades <= 0:  # Unidades deben ser entero positivo
            raise ServicioInvalidoError(f"Unidades inválidas: {unidades!r}")  # Error propio
        self._unidades = unidades  # Guarda las unidades disponibles

    def validar_parametros(self, horas):  # Sobrescribe la validación
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:  # Equipos: hasta 72 horas
            raise ServicioInvalidoError("Los equipos se alquilan de 1 a 72 horas")  # Error propio

    def calcular_costo(self, horas):  # Sobrescribe el costo
        self.validar_parametros(horas)  # Valida antes de calcular
        descuento = 0.85 if horas >= 24 else 1.0  # 15 % menos por alquiler de 24 horas o más
        return self._tarifa_hora * horas * descuento  # Costo base del equipo

    def describir(self):  # Sobrescribe la descripción
        return f"Equipo '{self._nombre}' ({self._unidades} unidades), ${self._tarifa_hora:,.0f}/hora"  # Texto


class AsesoriaEspecializada(Servicio):  # Servicio 3: asesorías
    NIVELES = {"basico": 1.0, "avanzado": 1.5, "experto": 2.0}  # Multiplicador por nivel

    def __init__(self, nombre, tarifa_hora, nivel):  # Constructor con nivel
        super().__init__(nombre, tarifa_hora)  # Datos comunes
        if nivel not in self.NIVELES:  # El nivel debe ser uno de los definidos
            raise ServicioInvalidoError(f"Nivel de asesoría inválido: {nivel!r}")  # Error propio
        self._nivel = nivel  # Guarda el nivel

    def validar_parametros(self, horas):  # Sobrescribe la validación
        if not isinstance(horas, (int, float)) or not 0.5 <= horas <= 6:  # Asesoría: 30 min a 6 horas
            raise ServicioInvalidoError("Las asesorías duran entre 0.5 y 6 horas")  # Error propio

    def calcular_costo(self, horas):  # Sobrescribe el costo
        self.validar_parametros(horas)  # Valida antes de calcular
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]  # Costo según nivel

    def describir(self):  # Sobrescribe la descripción
        return f"Asesoría '{self._nombre}' nivel {self._nivel}, ${self._tarifa_hora:,.0f}/hora"  # Texto
