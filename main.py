# ======================================================================================================================
# MÓDULO: main.py
# DESCRIPCIÓN: Programa principal que simula 18 operaciones del sistema Software FJ sin base de datos.
#              Demuestra estabilidad, robustez y manejo controlado de errores.
# AUTOR: Heiner Santana Muñoz - Grupo 62 - UNAD
# ======================================================================================================================

"""Programa principal: simula las operaciones del sistema Software FJ sin base de datos."""  # Docstring
from gestion.cliente import Cliente  # Clase de clientes
from gestion.excepciones import ErrorSoftwareFJ  # Excepción base del sistema
from gestion.reserva import Reserva  # Clase de reservas
from gestion.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala  # Servicios concretos
from gestion import logger  # Registro de eventos y errores


class SistemaFJ:  # Administra las listas internas de entidades
    """Gestor central de clientes, servicios y reservas."""  # Descripción

    def __init__(self):  # Constructor del sistema
        self.clientes = []  # Lista interna de clientes
        self.servicios = []  # Lista interna de servicios
        self.reservas = []  # Lista interna de reservas
        self.exitosas = 0  # Contador de operaciones exitosas
        self.fallidas = 0  # Contador de operaciones con error controlado

    def ejecutar(self, titulo, operacion):  # Ejecuta una operación sin detener el programa
        print(f"\n>> {titulo}")  # Muestra el título de la operación
        try:  # Intenta ejecutar la operación
            resultado = operacion()  # Llama a la función recibida
        except ErrorSoftwareFJ as error:  # Errores esperados del sistema
            self.fallidas += 1  # Cuenta la falla controlada
            logger.registrar_error(titulo, error)  # Escribe el error en el log
            print(f"   [ERROR CONTROLADO] {error}")  # Informa en pantalla
            if error.__cause__ is not None:  # Si hay una causa encadenada
                print(f"   Causa original: {error.__cause__}")  # Muestra la causa
        except Exception as error:  # Cualquier otro error inesperado
            self.fallidas += 1  # Cuenta la falla
            logger.registrar_error(f"{titulo} (inesperado): {error}")  # Registra el error
            print(f"   [ERROR INESPERADO] {error}")  # Informa en pantalla
        else:  # Sin errores
            self.exitosas += 1  # Cuenta el éxito
            logger.registrar_evento(f"OK: {titulo}")  # Registra el evento
            print(f"   [OK] {resultado}")  # Muestra el resultado
        finally:  # Se ejecuta siempre
            logger.registrar_evento(f"Fin de la operación: {titulo}")  # Marca de cierre

    def registrar_cliente(self, *datos):  # Crea y guarda un cliente
        cliente = Cliente(*datos)  # Puede lanzar ClienteInvalidoError
        self.clientes.append(cliente)  # Guarda en la lista
        return cliente.describir()  # Devuelve la descripción

    def agregar_servicio(self, servicio):  # Guarda un servicio ya creado
        self.servicios.append(servicio)  # Guarda en la lista
        return servicio.describir()  # Devuelve la descripción

    def reservar(self, cliente, servicio, horas, confirmar=True):  # Crea, procesa y confirma una reserva
        reserva = Reserva(cliente, servicio, horas)  # Puede lanzar ReservaError
        self.reservas.append(reserva)  # La guarda aunque falle, para dejar rastro
        reserva.procesar()  # Calcula el costo
        if confirmar:  # Si se pidió confirmar
            reserva.confirmar()  # Confirma la reserva
        return reserva.describir()  # Devuelve la descripción


def main():  # Función principal con la simulación
    s = SistemaFJ()  # Crea el sistema
    logger.registrar_evento("Inicio de la simulación de Software FJ")  # Evento inicial
    print("=== SOFTWARE FJ: simulación de operaciones ===")  # Encabezado

    # 1. Cliente válido
    s.ejecutar("1. Registro de cliente válido (Heiner Santana)",
               lambda: s.registrar_cliente("heiner santana", "1079654500", "hesantanam@unadvirtual.edu.co", "3001234567"))
    # 2. Cliente válido
    s.ejecutar("2. Registro de cliente válido (Laura Ospino)",
               lambda: s.registrar_cliente("Laura Ospino", "1045678123", "laura.ospino@correo.com", "3109876543"))
    # 3. Cliente inválido: correo mal formado
    s.ejecutar("3. Registro de cliente con correo inválido",
               lambda: s.registrar_cliente("Carlos Polo", "1122334455", "carlos.polo#correo", "3151112233"))
    # 4. Cliente inválido: documento con letras
    s.ejecutar("4. Registro de cliente con documento inválido",
               lambda: s.registrar_cliente("Ana Gómez", "12AB56", "ana@correo.com", "3201112233"))
    # 5. Servicios válidos
    s.ejecutar("5. Creación de sala de juntas (válida)",
               lambda: s.agregar_servicio(ReservaSala("Sala Magdalena", 80000, 25)))
    s.ejecutar("6. Creación de alquiler de portátiles (válido)",
               lambda: s.agregar_servicio(AlquilerEquipo("Portátil Dell", 12000, 10)))
    s.ejecutar("7. Creación de asesoría de redes (válida)",
               lambda: s.agregar_servicio(AsesoriaEspecializada("Asesoría en redes", 150000, "experto")))
    # 8. Servicio inválido: tarifa negativa
    s.ejecutar("8. Creación de servicio con tarifa negativa",
               lambda: s.agregar_servicio(AlquilerEquipo("Proyector", -5000, 3)))
    # 9. Servicio inválido: nivel inexistente
    s.ejecutar("9. Creación de asesoría con nivel inexistente",
               lambda: s.agregar_servicio(AsesoriaEspecializada("Asesoría cloud", 100000, "maestro")))

    c1, c2 = s.clientes[0], s.clientes[1]  # Clientes registrados correctamente
    sala, equipo, asesoria = s.servicios[0], s.servicios[1], s.servicios[2]  # Servicios creados correctamente

    # 10. Reserva exitosa
    s.ejecutar("10. Reserva exitosa de sala por 3 horas", lambda: s.reservar(c1, sala, 3))
    # 11. Reserva exitosa de equipo (con descuento por 24 h)
    s.ejecutar("11. Reserva exitosa de equipo por 30 horas", lambda: s.reservar(c2, equipo, 30))
    # 12. Reserva fallida: duración fuera de rango
    s.ejecutar("12. Reserva de asesoría con duración inválida (10 h)", lambda: s.reservar(c1, asesoria, 10))
    # 13. Reserva fallida: servicio no disponible
    equipo_fuera = AlquilerEquipo("Cámara 4K", 20000, 2)  # Servicio que se deshabilitará
    equipo_fuera.deshabilitar()  # Lo marca no disponible
    s.ejecutar("13. Reserva de servicio no disponible", lambda: s.reservar(c2, equipo_fuera, 2))
    # 14. Reserva fallida: parámetros faltantes
    s.ejecutar("14. Reserva sin cliente", lambda: s.reservar(None, sala, 2))
    # 15. Cancelación válida
    s.ejecutar("15. Cancelación de la primera reserva", lambda: (s.reservas[0].cancelar(), s.reservas[0].describir())[1])
    # 16. Operación no permitida: cancelar de nuevo
    s.ejecutar("16. Cancelar una reserva ya cancelada", lambda: s.reservas[0].cancelar())
    # 17. Cálculo con sobrecarga: horas, impuesto y descuento
    s.ejecutar("17. Costo total con impuesto 19 % y descuento 10 %",
               lambda: f"${asesoria.calcular_costo_total(2, 0.19, 0.10):,.2f}")
    # 18. Cálculo inconsistente: descuento mayor a 100 %
    s.ejecutar("18. Costo total con descuento inconsistente (150 %)",
               lambda: asesoria.calcular_costo_total(2, 0.19, 1.5))

    print("\n=== RESUMEN ===")  # Encabezado del resumen
    print(f"Operaciones exitosas: {s.exitosas} | Errores controlados: {s.fallidas}")  # Totales
    print(f"Clientes: {len(s.clientes)} | Servicios: {len(s.servicios)} | Reservas: {len(s.reservas)}")  # Listas
    print("El programa terminó sin interrupciones. Revisa logs/eventos.log")  # Cierre
    logger.registrar_evento("Fin de la simulación")  # Evento final


if __name__ == "__main__":  # Punto de entrada
    main()  # Ejecuta la simulación
