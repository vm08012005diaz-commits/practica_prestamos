# Práctica: Préstamo de equipo en Odoo

**Estudiante:** Madeline Lisbeth Perez Diaz  
**Asignatura:** Programación de Negocios  
**Versión objetivo:** Odoo 20.0

En este repositorio desarrollé el módulo `prestamo_unicah` paso a paso según la guía práctica. También incluí mis respuestas y las cuatro mejoras del reto.

## Respuestas

Estas son mis respuestas a las preguntas de cada paso.

### Paso 1. Catálogo de equipos

1. Cuando desmarco **Activo**, el registro se archiva. El equipo sigue en la base de datos, pero las vistas normales lo ocultan mediante el filtro de registros activos. Considero que es mejor archivarlo que borrarlo porque así conservo su historial y sus relaciones.
2. Entiendo que `copy=False` evita que el código de inventario se copie cuando duplico un equipo. De esta forma, el registro nuevo no hereda un identificador que debe ser único para cada activo.

### Paso 2. Registro de préstamos

1. Con `_name = "prestamo.prestamo"` creo un modelo y una tabla propios. Con `_inherit = ["mail.thread"]` le agrego al modelo las funciones del chatter y el seguimiento de cambios sin cambiar su identidad.
2. Al usar `tracking=True`, hago que los cambios del campo `state` queden registrados en el chatter, incluyendo el valor anterior, el valor nuevo, el usuario y la fecha.

### Paso 3. Equipos del préstamo

1. En `fields.One2many("prestamo.linea", "prestamo_id")`, identifico que el primer parámetro es el modelo relacionado y el segundo es el campo `Many2one` que apunta al préstamo actual.
2. Cuando borro un préstamo, también se borran sus líneas. Este comportamiento lo definí con `ondelete="cascade"` en el campo `prestamo_id` de `prestamo.linea`.

### Paso 4. Flujo de estados

1. Aunque oculto los botones según el estado, comprendo que esa es solamente una regla de interfaz y que una llamada RPC, una automatización o una llamada directa todavía podría ejecutar el método. Por eso vuelvo a validar el estado en el servidor y protejo los datos sin importar desde dónde se llame la acción.
2. Con `prestamo.linea_ids.equipo_id.write(...)` obtengo todas las líneas, llego a sus equipos y hago una escritura por lote sobre el recordset resultante. Por eso no necesito escribir un `for` para cada equipo.

### Paso 5. Reglas del préstamo

1. El dominio de `equipo_id` me ayuda a mostrar solamente equipos disponibles, pero no garantiza la integridad porque el estado puede cambiar después de elegirlos o los datos pueden llegar por importación, API o código. Por eso en el TODO 5 vuelvo a comprobar el estado justo antes de prestar.
2. Entiendo que un método con `@api.constrains` se ejecuta al crear o modificar un registro cuando cambia alguno de los campos indicados y bloquea el guardado si lanza `ValidationError`. En cambio, mi validación de `action_prestar` se ejecuta únicamente cuando presiono **Prestar**, justo antes de cambiar los estados.

### Paso 6. Contacto, kanban y búsqueda

1. Cuando arrastro una tarjeta a otra columna, Odoo escribe en `estado` el valor del nuevo grupo porque el kanban está agrupado por ese campo. Este cambio directo no ejecuta los botones del flujo, así que no debo usarlo para sustituir **Prestar** o **Devolver**, ya que esas acciones validan y sincronizan los equipos.
2. Al agregar `prestamo_ids` a `res.partner`, no creo una columna nueva en la tabla de contactos. El `One2many` es una relación inversa virtual que usa la columna `partner_id` de `prestamo.prestamo` para encontrar los préstamos de cada contacto.

## Reto

### 1. Marcar atrasado

Agregué el botón **Marcar atrasado**, visible solamente cuando el préstamo está Prestado. Antes de cambiar el estado comparo la fecha de devolución con la fecha actual mediante `fields.Date.context_today(self)`. Si la fecha todavía no ha pasado, muestro un `UserError`; si ya pasó, cambio el estado a Atrasado y dejo constancia en el chatter.

### 2. Colores en la lista

Agregué `decoration-danger` para mostrar en rojo los préstamos Atrasados y `decoration-muted` para mostrar en gris los Devueltos. Las expresiones dependen directamente del campo `state` de cada fila.

### 3. Veces prestado

Creé el campo calculado `veces_prestado` en el equipo. Para cada equipo cuento con `search_count` cuántas líneas de préstamo tienen su `equipo_id`. Muestro el resultado tanto en el formulario como en la tarjeta del kanban.

### 4. Mantenimiento

Agregué los botones **Enviar a mantenimiento** y **Marcar disponible** en el formulario del equipo. Cada botón aparece solamente en el estado correspondiente. Además, valido en el servidor que un equipo Prestado no pueda enviarse a mantenimiento y que solo uno que esté En mantenimiento pueda volver a Disponible.

