# ======================================================================================================================
# MÓDULO: cliente.py
# DESCRIPCIÓN: Clase Cliente con validaciones robustas y encapsulación estricta.
#              Hereda de la clase abstracta Entidad.
#              Valida nombre, cédula y email usando expresiones regulares.
# AUTOR: Heiner Santana Muñoz - Grupo 3 - UNAD
# ======================================================================================================================

import re
import logging
from abc import ABC, abstractmethod


# ======================================================================================================================
# CLASE ABSTRACTA: Entidad
# ======================================================================================================================

class Entidad(ABC):
    """
    Clase abstracta base que representa entidades generales del sistema.
    Obliga a las clases hijas a implementar el método describir().
    """
    
    def __init__(self, id_entidad: int):
        """
        Constructor de la clase Entidad.
        
        Args:
            id_entidad (int): Identificador único de la entidad.
        """
        self._id_entidad = id_entidad  # Atributo protegido (encapsulamiento)

    @property
    def id_entidad(self) -> int:
        """Getter del ID de la entidad."""
        return self._id_entidad

    @abstractmethod
    def describir(self) -> str:
        """
        Método abstracto que debe ser implementado por todas las clases hijas.
        Retorna una descripción en string de la entidad.
        """
        pass


# ======================================================================================================================
# EXCEPCIÓN PERSONALIZADA PARA CLIENTES
# ======================================================================================================================

class ClienteInvalidoError(Exception):
    """
    Excepción personalizada lanzada cuando los datos de un cliente
    no cumplen con las validaciones establecidas.
    """
    pass


# ======================================================================================================================
# CLASE CONCRETA: Cliente
# ======================================================================================================================

class Cliente(Entidad):
    """
    Clase que representa a un cliente del sistema Software FJ.
    Implementa encapsulamiento estricto con @property y @setter.
    Valida nombre, cédula y email al momento de la asignación.
    """
    
    def __init__(self, id_cliente: int, nombre: str, cedula: str, email: str):
        """
        Constructor de la clase Cliente.
        Llama al constructor de la clase padre (Entidad) y usa los setters
        para aplicar validaciones desde la inicialización.
        
        Args:
            id_cliente (int): Identificador único del cliente.
            nombre (str): Nombre completo del cliente.
            cedula (str): Número de cédula del cliente.
            email (str): Correo electrónico del cliente.
        """
        super().__init__(id_cliente)  # Llamada al constructor de la clase padre
        # Usamos los setters para aplicar validaciones automáticamente
        self.nombre = nombre
        self.cedula = cedula
        self.email = email
        logging.info(f"Cliente creado exitosamente: {self.nombre} (ID: {self.id_entidad})")

    # --- Encapsulamiento y Validaciones con @property ---

    @property
    def nombre(self) -> str:
        """Getter del nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        """
        Setter del nombre con validación.
        Valida que sea un string y tenga al menos 3 caracteres.
        """
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                f"Nombre inválido: '{valor}'. Debe ser un texto con al menos 3 caracteres."
            )
        self._nombre = valor.strip()  # Eliminamos espacios en blanco al inicio y final

    @property
    def cedula(self) -> str:
        """Getter de la cédula del cliente."""
        return self._cedula

    @cedula.setter
    def cedula(self, valor: str):
        """
        Setter de la cédula con validación.
        Valida que sea numérica y tenga al menos 5 dígitos.
        """
        if not valor.isdigit() or len(valor) < 5:
            raise ClienteInvalidoError(
                f"Cédula inválida: '{valor}'. Debe ser numérica y tener al menos 5 dígitos."
            )
        self._cedula = valor

    @property
    def email(self) -> str:
        """Getter del email del cliente."""
        return self._email

    @email.setter
    def email(self, valor: str):
        """
        Setter del email con validación usando expresión regular.
        Valida el formato estándar de correo electrónico.
        """
        # Expresión regular para validar formato de email
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex, valor):
            raise ClienteInvalidoError(
                f"Email inválido: '{valor}'. Formato incorrecto (ej: usuario@dominio.com)."
            )
        self._email = valor

    def describir(self) -> str:
        """
        Implementación del método abstracto de la clase Entidad.
        Retorna una descripción legible del cliente.
        """
        return f"Cliente ID {self.id_entidad}: {self.nombre} (CC: {self.cedula}, Email: {self.email})"

    def __str__(self):
        """Método especial para representación en string."""
        return self.describir()
