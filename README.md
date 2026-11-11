# Software FJ – Sistema integral de gestión de clientes, servicios y reservas

Proyecto del curso **Programación (213023)**, Fase 4 – Prácticas simuladas (UNAD).
Aplicación en Python orientada a objetos, **sin base de datos**: la información vive en objetos y listas, y el único archivo que se escribe es el registro de eventos y errores (`logs/eventos.log`).

## Ejecución
```bash
python main.py
```
Requiere Python 3.8 o superior. No usa librerías externas.

## Estructura
| Archivo | Contenido |
|---|---|
| `main.py` | Simulación de 18 operaciones válidas e inválidas (punto de entrada) |
| `gestion/__init__.py` | Archivo vacío que convierte la carpeta `gestion` en un paquete |
| `gestion/excepciones.py` | Jerarquía de excepciones personalizadas (`ErrorSoftwareFJ` y derivadas) |
| `gestion/logger.py` | Configuración del log de eventos y errores |
| `gestion/entidades.py` | Clase abstracta `EntidadBase` |
| `gestion/cliente.py` | `Cliente` con atributos privados y validaciones |
| `gestion/servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `gestion/reserva.py` | `Reserva` con procesar, confirmar y cancelar |

## Conceptos aplicados
- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`).
- **Herencia y polimorfismo:** tres servicios sobrescriben `calcular_costo`, `validar_parametros` y `describir`.
- **Encapsulación:** atributos privados y propiedades con validación en `Cliente`.
- **Sobrecarga:** `calcular_costo_total(horas)`, `(horas, impuesto)` y `(horas, impuesto, descuento)`.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.
- **Estabilidad:** `main.py` captura cada error, lo registra y continúa con la siguiente operación.
