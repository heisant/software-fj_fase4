# ======================================================================================================================
# MÓDULO: main.py
# DESCRIPCIÓN: Script principal que ejecuta las 10 pruebas de estrés del sistema Software FJ.
#              Demuestra el manejo robusto de excepciones, polimorfismo y logs.
#              Cumple con los requisitos del Anexo 3 de la Fase 4.
# AUTOR: Heiner Santana Muñoz - Grupo 3 - UNAD
# CURSO: Programación (213023)
# ======================================================================================================================

# Importamos el módulo logging nativo de Python para registrar eventos y errores en un archivo
import logging

# Importamos las clases y excepciones desde el paquete 'gestion' que creamos
from gestion import (
    Cliente, ReservaDeSala, AlquilerDeEquipo, AsesoriaEspecializada, Reserva,
    ClienteInvalidoError, ServicioNoDisponibleError, ReservaInvalidaError, TarifaInvalidaError
)


# ======================================================================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# ======================================================================================================================
# Configuramos el módulo logging para que guarde los eventos en un archivo de texto
# Esto cumple con el requisito de no usar bases de datos para el historial de errores
logging.basicConfig(
    filename='software_fj_logs.log',  # Nombre del archivo donde se guardarán los logs
    level=logging.INFO,               # Nivel mínimo de registro (INFO, WARNING, ERROR)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato de cada línea del log
    datefmt='%Y-%m-%d %H:%M:%S'       # Formato de la fecha y hora
)

# Agregamos un handler para que también se muestre en la consola en tiempo real
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)


# ======================================================================================================================
# FUNCIÓN AUXILIAR PARA IMPRIMIR SEPARADORES EN CONSOLA
# ======================================================================================================================
def imprimir_separador(mensaje: str):
    """
    Función auxiliar que imprime un separador visual en consola para cada prueba.
    Mejora la legibilidad de la salida durante la ejecución.
    """
    print("\n" + "=" * 70)
    print(f"  {mensaje}")
    print("=" * 70)


# ======================================================================================================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ======================================================================================================================
if __name__ == "__main__":
    # Registramos en el log el inicio de la simulación
    logging.info("INICIO DE SIMULACIÓN - SOFTWARE FJ (10 PRUEBAS DE ESTRÉS)")
    logging.info("Sistema Integral de Gestión - Fase 4 - UNAD")
    
    # Lista en memoria para simular la "base de datos" de clientes, servicios y reservas
    # (Requisito del Anexo 3: no usar bases de datos, solo objetos y listas)
    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    # ==================================================================================================================
    # OPERACIÓN 1: Registro VÁLIDO de cliente
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 1: Registro VÁLIDO de cliente")
    try:
        # Creamos un cliente con datos correctos
        cliente1 = Cliente(1, "Heiner Santana", "1079654500", "heiner.santana@unad.edu.co")
        lista_clientes.append(cliente1)  # Agregamos a la lista en memoria
        logging.info(f"Op 1 - Cliente registrado exitosamente: {cliente1.nombre}")
        print(f"✅ Cliente creado: {cliente1}")
    except ClienteInvalidoError as e:
        # Si hay error, lo capturamos y lo registramos en el log
        logging.error(f"Op 1 - Error al registrar cliente: {e}")
        print(f"❌ Error: {e}")

    # ==================================================================================================================
    # OPERACIÓN 2: Registro INVÁLIDO de cliente (Email mal formado)
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 2: Registro INVÁLIDO de cliente (Email mal formado)")
    try:
        # Intentamos crear un cliente con un email sin dominio válido (falta el .com)
        cliente2 = Cliente(2, "Juan Perez", "1234567", "juan.perez@correo")
        lista_clientes.append(cliente2)
        logging.info(f"Op 2 - Cliente registrado: {cliente2.nombre}")
    except ClienteInvalidoError as e:
        # Capturamos la excepción personalizada y el programa NO se cierra
        logging.error(f"Op 2 - Error capturado correctamente: {e}")
        print(f"✅ Excepción capturada: {e}")

    # ==================================================================================================================
    # OPERACIÓN 3: Registro INVÁLIDO de cliente (Cédula con letras)
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 3: Registro INVÁLIDO de cliente (Cédula con letras)")
    try:
        # Intentamos crear un cliente con cédula que contiene letras
        cliente3 = Cliente(3, "Maria Lopez", "ABC123", "maria@correo.com")
        lista_clientes.append(cliente3)
    except ClienteInvalidoError as e:
        logging.error(f"Op 3 - Error capturado correctamente: {e}")
        print(f"✅ Excepción capturada: {e}")

    # ==================================================================================================================
    # OPERACIÓN 4: Creación CORRECTA de servicios (Polimorfismo)
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 4: Creación CORRECTA de 3 servicios especializados")
    try:
        # Creamos los 3 tipos de servicios especializados (Polimorfismo en acción)
        sala1 = ReservaDeSala(101, "Sala de Juntas A", 50000, 10)
        equipo1 = AlquilerDeEquipo(201, "Proyector 4K", 30000, "Video")
        asesoria1 = AsesoriaEspecializada(301, "Consultoría Python", 150000, "Desarrollo")
        
        # Agregamos a la lista en memoria
        lista_servicios.extend([sala1, equipo1, asesoria1])
        
        # Mostramos la descripción polimórfica de cada servicio
        for servicio in lista_servicios:
            print(f"✅ {servicio.describir()}")
            logging.info(f"Op 4 - Servicio registrado: {servicio.nombre}")
    except Exception as e:
        logging.error(f"Op 4 - Error inesperado: {e}")
        print(f"❌ Error: {e}")

    # ==================================================================================================================
    # OPERACIÓN 5: Creación INCORRECTA de servicio (Tarifa base negativa)
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 5: Creación INCORRECTA de servicio (Tarifa negativa)")
    try:
        # Intentamos crear un servicio con tarifa negativa (debería fallar)
        sala2 = ReservaDeSala(102, "Sala B", -10000, 5)
        lista_servicios.append(sala2)
    except TarifaInvalidaError as e:
        # Capturamos la excepción personalizada del setter de tarifa_base
        logging.error(f"Op 5 - Error capturado correctamente: {e}")
        print(f"✅ Excepción capturada: {e}")

    # ==================================================================================================================
    # OPERACIÓN 6: Reserva EXITOSA con confirmación y procesamiento
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 6: Reserva EXITOSA (try/except/else/finally)")
    try:
        # Creamos una reserva válida: cliente1 reserva la sala1 por 3 horas
        reserva1 = Reserva(1001, cliente1, sala1, 3)
        lista_reservas.append(reserva1)
        
        # Confirmamos la reserva (valida disponibilidad y duración)
        reserva1.confirmar()
        
        # Procesamos la reserva (calcula el costo usando try/except/else/finally)
        costo_total = reserva1.procesar()
        
        print(f"✅ Reserva confirmada. Costo total: ${costo_total}")
        logging.info(f"Op 6 - Reserva exitosa. Costo: ${costo_total}")
    except ReservaInvalidaError as e:
        logging.error(f"Op 6 - Error en reserva: {e}")
        print(f"❌ Error: {e}")

    # ==================================================================================================================
    # OPERACIÓN 7: Reserva FALLIDA (Servicio no disponible)
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 7: Reserva FALLIDA (Servicio no disponible)")
    try:
        # Simulamos que el proyector se dañó y no está disponible
        equipo1.disponible = False
        logging.info("Op 7 - Equipo marcado como NO disponible")
        
        # Intentamos crear y confirmar una reserva con el equipo no disponible
        reserva2 = Reserva(1002, cliente1, equipo1, 2)
        lista_reservas.append(reserva2)
        reserva2.confirmar()  # Esto debe lanzar ServicioNoDisponibleError
        
    except ServicioNoDisponibleError as e:
        # Capturamos la excepción y el programa sigue funcionando
        logging.error(f"Op 7 - Error capturado correctamente: {e}")
        print(f"✅ Excepción capturada: {e}")

    # ==================================================================================================================
    # OPERACIÓN 8: Prueba de POLIMORFISMO (Mismo método, distinto comportamiento)
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 8: Prueba de POLIMORFISMO en calcular_costo()")
    try:
        # Restauramos la disponibilidad del equipo para la prueba
        equipo1.disponible = True
        
        # Llamamos al mismo método calcular_costo() en 3 objetos distintos
        # Cada uno usa su propia lógica (horas, días, sesiones)
        costo_sala = sala1.calcular_costo(horas=2)
        costo_equipo = equipo1.calcular_costo(dias=1)
        costo_asesoria = asesoria1.calcular_costo(sesiones=3)
        
        print(f"✅ Sala (2h): ${costo_sala}")
        print(f"✅ Equipo (1d): ${costo_equipo}")
        print(f"✅ Asesoría (3 sesiones): ${costo_asesoria}")
        logging.info(f"Op 8 - Polimorfismo: Sala=${costo_sala}, Equipo=${costo_equipo}, Asesoría=${costo_asesoria}")
    except Exception as e:
        logging.error(f"Op 8 - Error: {e}")
        print(f"❌ Error: {e}")

    # ==================================================================================================================
    # OPERACIÓN 9: Prueba de SOBRECARGA SIMULADA (Argumentos opcionales)
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 9: Sobrecarga simulada (con/sin descuentos e impuestos)")
    try:
        # Llamada 1: Solo parámetro principal (usa valores por defecto)
        costo_normal = sala1.calcular_costo(horas=2)
        
        # Llamada 2: Con descuento del 20% y sin impuestos (simula otra "sobrecarga")
        costo_descuento = sala1.calcular_costo(horas=2, descuento=0.20, impuestos=0.0)
        
        print(f"✅ Costo normal (2h): ${costo_normal}")
        print(f"✅ Costo con 20% desc y 0% imp: ${costo_descuento}")
        logging.info(f"Op 9 - Sobrecarga: Normal=${costo_normal}, ConDesc=${costo_descuento}")
    except Exception as e:
        logging.error(f"Op 9 - Error: {e}")
        print(f"❌ Error: {e}")

    # ==================================================================================================================
    # OPERACIÓN 10: Cancelación VÁLIDA y luego cancelación INVÁLIDA (doble cancelación)
    # ==================================================================================================================
    imprimir_separador("OPERACIÓN 10: Cancelación válida e inválida (doble cancelación)")
    try:
        # Cancelación válida de la reserva1
        reserva1.cancelar()
        print(f"✅ Reserva {reserva1.id_reserva} cancelada exitosamente. Estado: {reserva1.estado}")
        logging.info(f"Op 10 - Reserva cancelada: {reserva1.id_reserva}")
        
        # Intentamos cancelar la misma reserva nuevamente (debe fallar)
        print("\n⚠️ Intentando cancelar nuevamente la misma reserva...")
        reserva1.cancelar()  # Esto debe lanzar ReservaInvalidaError
        
    except ReservaInvalidaError as e:
        # Capturamos la excepción de doble cancelación
        logging.error(f"Op 10 - Error capturado correctamente: {e}")
        print(f"✅ Excepción capturada: {e}")

    # ==================================================================================================================
    # RESUMEN FINAL
    # ==================================================================================================================
    imprimir_separador("RESUMEN FINAL DE LA SIMULACIÓN")
    print(f"📊 Total de clientes registrados: {len(lista_clientes)}")
    print(f"📊 Total de servicios registrados: {len(lista_servicios)}")
    print(f"📊 Total de reservas creadas: {len(lista_reservas)}")
    print(f"\n📝 Revisa el archivo 'software_fj_logs.log' para ver el historial completo de eventos.")
    
    logging.info("=" * 70)
    logging.info("FIN DE SIMULACIÓN - SOFTWARE FJ")
    logging.info("=" * 70)
    print("\n🎉 ¡Simulación completada exitosamente! El sistema manejó todos los errores sin colapsar.")
