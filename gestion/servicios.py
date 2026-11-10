# ======================================================================================================================
# MÓDULO: servicios.py
# DESCRIPCIÓN: Define la clase abstracta Servicio y sus 3 clases hijas especializadas.
#              Implementa polimorfismo, encapsulamiento y simulación de sobrecarga de métodos.
# AUTOR: Heiner Santana Muñoz - Grupo 3 - UNAD
# ======================================================================================================================

import logging
from abc import ABC, abstractmethod


# ======================================================================================================================
# EXCEPCIONES PERSONALIZADAS PARA SERVICIOS
# ======================================================================================================================

class TarifaInvalidaError(Exception):
    """
    Excepción personalizada lanzada cuando la tarifa base de un servicio 
    es negativa o cero.
    """
    pass

class ParametroServicioError(Exception):
    """
    Excepción personalizada lanzada cuando los parámetros de cálculo 
    (horas, días, sesiones) son inválidos.
    """
    pass


# ======================================================================================================================
# CLASE ABSTRACTA: Servicio
# ======================================================================================================================

class Servicio(ABC):
    """
    Clase abstracta base que define la estructura y comportamiento común 
    para todos los servicios ofrecidos por Software FJ.
    Obliga a las clases hijas a implementar calcular_costo() y describir().
    """
    
    def __init__(self, id_servicio: int, nombre: str, tarifa_base: float):
        """
        Constructor de la clase Servicio.
        
        Args:
            id_servicio (int): Identificador único del servicio.
            nombre (str): Nombre descriptivo del servicio.
            tarifa_base (float): Costo base por unidad de tiempo (hora/día/sesión).
        """
        self._id_servicio = id_servicio
        self.nombre = nombre
        # Usamos el setter para aplicar la validación de tarifa desde el inicio
        self.tarifa_base = tarifa_base
        self.disponible = True  # Estado inicial: el servicio está disponible
        
        logging.info(f"Servicio base creado: {self.nombre} (ID: {self._id_servicio})")

    # --- Encapsulamiento y Validaciones ---

    @property
    def id_servicio(self) -> int:
        """Getter del ID del servicio."""
        return self._id_servicio

    @property
    def tarifa_base(self) -> float:
        """Getter de la tarifa base."""
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float):
        """
        Setter de la tarifa base con validación estricta.
        Lanza TarifaInvalidaError si el valor es menor o igual a cero.
        """
        if valor <= 0:
            raise TarifaInvalidaError(f"La tarifa base debe ser mayor a cero. Valor recibido: {valor}")
        self._tarifa_base = valor

    # --- Métodos Abstractos (Polimorfismo) ---

    @abstractmethod
    def calcular_costo(self, **kwargs) -> float:
        """
        Método abstracto para calcular el costo del servicio.
        Se implementará de forma distinta en cada clase hija (Polimorfismo).
        Se usa **kwargs para simular sobrecarga de métodos en Python.
        """
        pass

    @abstractmethod
    def describir(self) -> str:
        """
        Método abstracto para retornar una descripción legible del servicio.
        """
        pass


# ======================================================================================================================
# CLASES CONCRETAS (Herencia y Polimorfismo)
# ======================================================================================================================

class ReservaDeSala(Servicio):
    """
    Clase especializada para el servicio de Reserva de Salas.
    Hereda de Servicio y agrega el atributo 'capacidad'.
    """
    
    def __init__(self, id_servicio: int, nombre: str, tarifa_base: float, capacidad: int):
        """Constructor específico para salas."""
        super().__init__(id_servicio, nombre, tarifa_base)
        self.capacidad = capacidad

    def calcular_costo(self, horas: int = 1, descuento: float = 0.0, impuestos: float = 0.19) -> float:
        """
        Calcula el costo de la sala basado en horas.
        Simulación de sobrecarga: acepta argumentos opcionales (descuento, impuestos).
        
        Args:
            horas (int): Número de horas de reserva.
            descuento (float): Porcentaje de descuento (0.0 a 1.0).
            impuestos (float): Porcentaje de impuestos (ej. 0.19 para 19%).
            
        Returns:
            float: Costo total calculado.
        """
        if horas <= 0:
            raise ParametroServicioError(f"Las horas deben ser mayores a cero. Recibido: {horas}")
        
        # Cálculo con descuentos e impuestos
        costo_base = self.tarifa_base * horas
        costo_con_descuento = costo_base * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuestos)
        
        logging.info(f"Costo calculado para Sala '{self.nombre}': ${round(costo_final, 2)}")
        return round(costo_final, 2)

    def describir(self) -> str:
        """Implementación polimórfica del método describir."""
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} personas | Tarifa/hora: ${self.tarifa_base}"


class AlquilerDeEquipo(Servicio):
    """
    Clase especializada para el servicio de Alquiler de Equipos.
    Hereda de Servicio y agrega el atributo 'tipo_equipo'.
    """
    
    def __init__(self, id_servicio: int, nombre: str, tarifa_base: float, tipo_equipo: str):
        """Constructor específico para equipos."""
        super().__init__(id_servicio, nombre, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias: int = 1, descuento: float = 0.0, impuestos: float = 0.19) -> float:
        """
        Calcula el costo del equipo basado en días.
        Polimorfismo: la lógica cambia respecto a la sala (usa días en vez de horas).
        """
        if dias <= 0:
            raise ParametroServicioError(f"Los días deben ser mayores a cero. Recibido: {dias}")
        
        costo_final = (self.tarifa_base * dias * (1 - descuento)) * (1 + impuestos)
        logging.info(f"Costo calculado para Equipo '{self.nombre}': ${round(costo_final, 2)}")
        return round(costo_final, 2)

    def describir(self) -> str:
        """Implementación polimórfica del método describir."""
        return f"Equipo: {self.nombre} | Tipo: {self.tipo_equipo} | Tarifa/día: ${self.tarifa_base}"


class AsesoriaEspecializada(Servicio):
    """
    Clase especializada para el servicio de Asesorías.
    Hereda de Servicio y agrega el atributo 'area_experticia'.
    """
    
    def __init__(self, id_servicio: int, nombre: str, tarifa_base: float, area_experticia: str):
        """Constructor específico para asesorías."""
        super().__init__(id_servicio, nombre, tarifa_base)
        self.area_experticia = area_experticia

    def calcular_costo(self, sesiones: int = 1, descuento: float = 0.0, impuestos: float = 0.19) -> float:
        """
        Calcula el costo de la asesoría basado en sesiones.
        Polimorfismo: la lógica cambia respecto a sala y equipo (usa sesiones).
        """
        if sesiones <= 0:
            raise ParametroServicioError(f"Las sesiones deben ser mayores a cero. Recibido: {sesiones}")
        
        costo_final = (self.tarifa_base * sesiones * (1 - descuento)) * (1 + impuestos)
        logging.info(f"Costo calculado para Asesoría '{self.nombre}': ${round(costo_final, 2)}")
        return round(costo_final, 2)

    def describir(self) -> str:
        """Implementación polimórfica del método describir."""
        return f"Asesoría: {self.nombre} | Área: {self.area_experticia} | Tarifa/sesión: ${self.tarifa_base}"
