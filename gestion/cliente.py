"""Clase Cliente con validaciones robustas y datos encapsulados."""  # Docstring del módulo
import re  # Expresiones regulares para validar formatos

from .entidades import EntidadBase  # Clase abstracta base
from .excepciones import ClienteInvalidoError  # Excepción propia de clientes


class Cliente(EntidadBase):  # El cliente es una entidad del sistema
    """Cliente de Software FJ con datos personales privados."""  # Descripción

    _familia = "cliente"  # Tipo de entidad para el contador de ids
    PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")  # Formato válido de correo

    def __init__(self, nombre, documento, correo, telefono):  # Constructor con datos personales
        super().__init__()  # Genera el id mediante la clase base
        self.nombre = nombre  # Pasa por el setter que valida el nombre
        self.documento = documento  # Pasa por el setter que valida el documento
        self.correo = correo  # Pasa por el setter que valida el correo
        self.telefono = telefono  # Pasa por el setter que valida el teléfono

    @property  # Getter del nombre
    def nombre(self):  # Devuelve el nombre privado
        return self.__nombre  # Atributo privado (name mangling)

    @nombre.setter  # Setter con validación
    def nombre(self, valor):  # Recibe el nuevo nombre
        if not isinstance(valor, str) or len(valor.strip()) < 3:  # Debe ser texto de al menos 3 letras
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r}")  # Lanza error propio
        if any(c.isdigit() for c in valor):  # El nombre no debe contener números
            raise ClienteInvalidoError("El nombre no puede contener números")  # Lanza error propio
        self.__nombre = valor.strip().title()  # Guarda el nombre normalizado

    @property  # Getter del documento
    def documento(self):  # Devuelve el documento privado
        return self.__documento  # Atributo privado

    @documento.setter  # Setter con validación
    def documento(self, valor):  # Recibe el nuevo documento
        if not str(valor).isdigit() or not 6 <= len(str(valor)) <= 10:  # Solo dígitos, de 6 a 10
            raise ClienteInvalidoError(f"Documento inválido: {valor!r}")  # Lanza error propio
        self.__documento = str(valor)  # Guarda el documento como texto

    @property  # Getter del correo
    def correo(self):  # Devuelve el correo privado
        return self.__correo  # Atributo privado

    @correo.setter  # Setter con validación
    def correo(self, valor):  # Recibe el nuevo correo
        if not isinstance(valor, str) or not self.PATRON_CORREO.match(valor):  # Verifica el formato
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")  # Lanza error propio
        self.__correo = valor.lower()  # Guarda el correo en minúsculas

    @property  # Getter del teléfono
    def telefono(self):  # Devuelve el teléfono privado
        return self.__telefono  # Atributo privado

    @telefono.setter  # Setter con validación
    def telefono(self, valor):  # Recibe el nuevo teléfono
        if not str(valor).isdigit() or len(str(valor)) != 10:  # Celular colombiano de 10 dígitos
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r}")  # Lanza error propio
        self.__telefono = str(valor)  # Guarda el teléfono como texto

    def describir(self):  # Implementa el método abstracto
        return f"Cliente #{self.id}: {self.nombre} (doc. {self.documento}, {self.correo})"  # Resumen del cliente
