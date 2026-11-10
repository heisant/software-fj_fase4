# ======================================================================================================================
# MÓDULO: logger.py
# DESCRIPCIÓN: Configuración del archivo de logs para eventos y errores. Crea la carpeta 'logs' 
#              si no existe y define funciones para registrar con diferentes niveles de severidad.
# AUTOR: Heiner Santana Muñoz - Grupo 3 - UNAD
# ======================================================================================================================

"""Configuración del archivo de logs para eventos y errores."""  # Docstring del módulo
import logging  # Módulo estándar de registro de eventos
import os  # Módulo para manejar rutas de carpetas

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Carpeta raíz del proyecto (un nivel sobre gestion)
RUTA_LOGS = os.path.join(RAIZ, "logs")  # Carpeta logs en la raíz del proyecto
os.makedirs(RUTA_LOGS, exist_ok=True)  # Crea la carpeta si no existe
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "eventos.log")  # Ruta completa del archivo de log

_logger = logging.getLogger("software_fj")  # Obtiene el logger principal del sistema
_logger.setLevel(logging.INFO)  # Registra desde el nivel INFO hacia arriba
if not _logger.handlers:  # Evita duplicar manejadores si se importa varias veces
    _manejador = logging.FileHandler(ARCHIVO_LOG, mode="w", encoding="utf-8")  # Archivo nuevo en cada ejecución
    _manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))  # Formato de cada línea
    _logger.addHandler(_manejador)  # Asocia el manejador al logger


def registrar_evento(mensaje):  # Registra un evento normal
    _logger.info(mensaje)  # Escribe la línea con nivel INFO


def registrar_advertencia(mensaje):  # Registra una situación anómala no crítica
    _logger.warning(mensaje)  # Escribe la línea con nivel WARNING


def registrar_error(mensaje, excepcion=None):  # Registra un error con su causa si existe
    if excepcion is not None:  # Si se recibió la excepción original
        causa = excepcion.__cause__  # Obtiene la excepción encadenada (raise ... from ...)
        codigo = getattr(excepcion, "codigo", "FJ-999")  # Toma el código o usa uno genérico
        texto = f"[{codigo}] {mensaje} -> {type(excepcion).__name__}: {excepcion}"  # Arma el texto del error
        if causa is not None:  # Si el error tiene una causa encadenada
            texto += f" | causa: {type(causa).__name__}: {causa}"  # Agrega la causa al texto
        _logger.error(texto)  # Escribe la línea con nivel ERROR
    else:  # Si no hay excepción asociada
        _logger.error(mensaje)  # Escribe solo el mensaje
