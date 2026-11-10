# ======================================================================================================================
# MÓDULO: cliente.py
# DESCRIPCIÓN: Clase Cliente con validaciones robustas y encapsulación estricta. 
#              Hereda de EntidadBase y valida nombre, documento, correo y teléfono.
# AUTOR: Heiner Santana Muñoz - Grupo 62 - UNAD
# ======================================================================================================================

import re
from .entidades import EntidadBase
from .excepciones import ClienteInvalidoError

class Cliente(EntidadBase):
    """Cliente de Software FJ con datos personales privados."""
    _familia = "cliente"
    PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r}")
        if any(c.isdigit() for c in valor):
            raise ClienteInvalidoError("El nombre no puede contener números")
        self.__nombre = valor.strip().title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not str(valor).isdigit() or not 6 <= len(str(valor)) <= 10:
            raise ClienteInvalidoError(f"Documento inválido: {valor!r}")
        self.__documento = str(valor)

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not self.PATRON_CORREO.match(valor):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__correo = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not str(valor).isdigit() or len(str(valor)) != 10:
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r}")
        self.__telefono = str(valor)

    def describir(self):
        return f"Cliente #{self.id}: {self.nombre} (doc. {self.documento}, {self.correo})"
