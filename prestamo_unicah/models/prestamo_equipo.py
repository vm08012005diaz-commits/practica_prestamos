from odoo import fields, models
from odoo.exceptions import UserError


class PrestamoEquipo(models.Model):
    _name = "prestamo.equipo"
    _description = "Equipo para préstamo"

    name = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código de inventario", required=True, copy=False)
    categoria = fields.Selection(
        [
            ("laptop", "Laptop"),
            ("proyector", "Proyector"),
            ("audio", "Audio"),
            ("laboratorio", "Laboratorio"),
        ],
        string="Categoría",
        required=True,
        default="laptop",
    )
    estado = fields.Selection(
        [
            ("disponible", "Disponible"),
            ("prestado", "Prestado"),
            ("mantenimiento", "En mantenimiento"),
        ],
        string="Estado",
        required=True,
        default="disponible",
    )
    notas = fields.Text(string="Notas")
    active = fields.Boolean(string="Activo", default=True)
    veces_prestado = fields.Integer(
        string="Veces prestado", compute="_compute_veces_prestado"
    )

    def _compute_veces_prestado(self):
        Linea = self.env["prestamo.linea"]
        for equipo in self:
            equipo.veces_prestado = Linea.search_count(
                [("equipo_id", "=", equipo.id)]
            )

    def action_enviar_mantenimiento(self):
        for equipo in self:
            if equipo.estado == "prestado":
                raise UserError(
                    "Un equipo prestado no se puede enviar a mantenimiento."
                )
            equipo.estado = "mantenimiento"

    def action_marcar_disponible(self):
        for equipo in self:
            if equipo.estado != "mantenimiento":
                raise UserError(
                    "Solo un equipo en mantenimiento se puede marcar como disponible."
                )
            equipo.estado = "disponible"
