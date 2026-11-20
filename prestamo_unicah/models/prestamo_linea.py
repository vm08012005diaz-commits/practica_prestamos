from odoo import fields, models


class PrestamoLinea(models.Model):
    _name = "prestamo.linea"
    _description = "Equipo del préstamo"

    prestamo_id = fields.Many2one(
        "prestamo.prestamo", string="Préstamo", required=True, ondelete="cascade"
    )
    equipo_id = fields.Many2one(
        "prestamo.equipo",
        string="Equipo",
        required=True,
        domain="[('estado', '=', 'disponible')]",
    )
    categoria = fields.Selection(
        related="equipo_id.categoria", string="Categoría", readonly=True
    )
    observacion = fields.Char(string="Observación")
