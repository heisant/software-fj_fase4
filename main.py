# ======================================================================================================================
# MÓDULO: main.py
# DESCRIPCIÓN: Programa principal que simula 18 operaciones del sistema Software FJ sin base de datos.
#              Demuestra estabilidad, robustez y manejo controlado de errores.
# AUTOR: Heiner Santana Muñoz - Grupo 3 - UNAD
# ======================================================================================================================

from gestion.cliente import Cliente
from gestion.excepciones import ErrorSoftwareFJ
from gestion.reserva import Reserva
from gestion.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
from gestion import logger

class SistemaFJ:
    """Gestor central de clientes, servicios y reservas."""
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.exitosas = 0
        self.fallidas = 0

    def ejecutar(self, titulo, operacion):
        print(f"\n>> {titulo}")
        try:
            resultado = operacion()
        except ErrorSoftwareFJ as error:
            self.fallidas += 1
            logger.registrar_error(titulo, error)
            print(f"   [ERROR CONTROLADO] {error}")
            if error.__cause__ is not None:
                print(f"   Causa original: {error.__cause__}")
        except Exception as error:
            self.fallidas += 1
            logger.registrar_error(f"{titulo} (inesperado): {error}")
            print(f"   [ERROR INESPERADO] {error}")
        else:
            self.exitosas += 1
            logger.registrar_evento(f"OK: {titulo}")
            print(f"   [OK] {resultado}")
        finally:
            logger.registrar_evento(f"Fin de la operación: {titulo}")

    def registrar_cliente(self, *datos):
        cliente = Cliente(*datos)
        self.clientes.append(cliente)
        return cliente.describir()

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        return servicio.describir()

    def reservar(self, cliente, servicio, horas, confirmar=True):
        reserva = Reserva(cliente, servicio, horas)
        self.reservas.append(reserva)
        reserva.procesar()
        if confirmar:
            reserva.confirmar()
        return reserva.describir()

def main():
    s = SistemaFJ()
    logger.registrar_evento("Inicio de la simulación de Software FJ")
    print("=== SOFTWARE FJ: simulación de operaciones ===")

    s.ejecutar("1. Registro de cliente válido (Heiner Santana)",
               lambda: s.registrar_cliente("heiner santana", "1079654500", "hesantanam@unadvirtual.edu.co", "3001234567"))
    s.ejecutar("2. Registro de cliente válido (Laura Ospino)",
               lambda: s.registrar_cliente("Laura Ospino", "1045678123", "laura.ospino@correo.com", "3109876543"))
    s.ejecutar("3. Registro de cliente con correo inválido",
               lambda: s.registrar_cliente("Carlos Polo", "1122334455", "carlos.polo#correo", "3151112233"))
    s.ejecutar("4. Registro de cliente con documento inválido",
               lambda: s.registrar_cliente("Ana Gómez", "12AB56", "ana@correo.com", "3201112233"))
    s.ejecutar("5. Creación de sala de juntas (válida)",
               lambda: s.agregar_servicio(ReservaSala("Sala Magdalena", 80000, 25)))
    s.ejecutar("6. Creación de alquiler de portátiles (válido)",
               lambda: s.agregar_servicio(AlquilerEquipo("Portátil Dell", 12000, 10)))
    s.ejecutar("7. Creación de asesoría de redes (válida)",
               lambda: s.agregar_servicio(AsesoriaEspecializada("Asesoría en redes", 150000, "experto")))
    s.ejecutar("8. Creación de servicio con tarifa negativa",
               lambda: s.agregar_servicio(AlquilerEquipo("Proyector", -5000, 3)))
    s.ejecutar("9. Creación de asesoría con nivel inexistente",
               lambda: s.agregar_servicio(AsesoriaEspecializada("Asesoría cloud", 100000, "maestro")))

    c1, c2 = s.clientes[0], s.clientes[1]
    sala, equipo, asesoria = s.servicios[0], s.servicios[1], s.servicios[2]

    s.ejecutar("10. Reserva exitosa de sala por 3 horas", lambda: s.reservar(c1, sala, 3))
    s.ejecutar("11. Reserva exitosa de equipo por 30 horas", lambda: s.reservar(c2, equipo, 30))
    s.ejecutar("12. Reserva de asesoría con duración inválida (10 h)", lambda: s.reservar(c1, asesoria, 10))
    
    equipo_fuera = AlquilerEquipo("Cámara 4K", 20000, 2)
    equipo_fuera.deshabilitar()
    s.ejecutar("13. Reserva de servicio no disponible", lambda: s.reservar(c2, equipo_fuera, 2))
    
    s.ejecutar("14. Reserva sin cliente", lambda: s.reservar(None, sala, 2))
    s.ejecutar("15. Cancelación de la primera reserva", lambda: (s.reservas[0].cancelar(), s.reservas[0].describir())[1])
    s.ejecutar("16. Cancelar una reserva ya cancelada", lambda: s.reservas[0].cancelar())
    s.ejecutar("17. Costo total con impuesto 19 % y descuento 10 %",
               lambda: f"${asesoria.calcular_costo_total(2, 0.19, 0.10):,.2f}")
    s.ejecutar("18. Costo total con descuento inconsistente (150 %)",
               lambda: asesoria.calcular_costo_total(2, 0.19, 1.5))

    print("\n=== RESUMEN ===")
    print(f"Operaciones exitosas: {s.exitosas} | Errores controlados: {s.fallidas}")
    print(f"Clientes: {len(s.clientes)} | Servicios: {len(s.servicios)} | Reservas: {len(s.reservas)}")
    print("El programa terminó sin interrupciones. Revisa logs/eventos.log")
    logger.registrar_evento("Fin de la simulación")

if __name__ == "__main__":
    main()
