# Práctica: Préstamo de equipo en Odoo

**Estudiante:** Madeline Lisbeth Perez Diaz  
**Asignatura:** Programación de Negocios  
**Versión objetivo:** Odoo 20.0

Este repositorio contiene el módulo `prestamo_unicah`, desarrollado paso a paso según la guía práctica, junto con las respuestas y las cuatro mejoras del reto.

## Respuestas

Las respuestas de cada paso se documentan en este archivo conforme avanza la práctica.

### Paso 1. Catálogo de equipos

1. Al desmarcar **Activo**, el registro se archiva: sigue en la base de datos, pero las vistas normales lo ocultan mediante el filtro implícito de registros activos. Es mejor que borrarlo porque conserva el historial y las relaciones del equipo.
2. `copy=False` evita que el código de inventario se copie al duplicar un equipo. Así, el nuevo registro no hereda un identificador que debe ser único para cada activo.

