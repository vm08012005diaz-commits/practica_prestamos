from odoo import api, fields, models
from odoo.exceptions import UserError


class PrestamoPrestamo(models.Model):
    _name = "prestamo.prestamo"
    _description = "Préstamo de equipo"
    _inherit = ["mail.thread"]
    _order = "fecha_prestamo desc, id desc"

    name = fields.Char(string="Motivo", required=True)
    partner_id = fields.Many2one("res.partner", string="Solicitante", required=True)
    tipo_solicitante = fields.Selection(
        [("estudiante", "Estudiante"), ("docente", "Docente")],
        string="Tipo de solicitante",
        required=True,
        default="estudiante",
    )
    fecha_prestamo = fields.Date(
        string="Fecha de préstamo", required=True, default=fields.Date.context_today
    )
    fecha_devolucion = fields.Date(string="Fecha de devolución", required=True)
    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("prestado", "Prestado"),
            ("devuelto", "Devuelto"),
            ("atrasado", "Atrasado"),
        ],
        string="Estado",
        required=True,
        default="borrador",
        tracking=True,
    )
    linea_ids = fields.One2many(
        "prestamo.linea", "prestamo_id", string="Equipos"
    )
    cantidad_equipos = fields.Integer(
        string="Cantidad de equipos", compute="_compute_cantidad_equipos", store=True
    )
    dias_prestamo = fields.Integer(
        string="Días de préstamo", compute="_compute_dias_prestamo", store=True
    )

    @api.depends("linea_ids")
    def _compute_cantidad_equipos(self):
        for prestamo in self:
            prestamo.cantidad_equipos = len(prestamo.linea_ids)

    @api.depends("fecha_prestamo", "fecha_devolucion")
    def _compute_dias_prestamo(self):
        for prestamo in self:
            if prestamo.fecha_prestamo and prestamo.fecha_devolucion:
                prestamo.dias_prestamo = (
                    prestamo.fecha_devolucion - prestamo.fecha_prestamo
                ).days
            else:
                prestamo.dias_prestamo = 0

    def action_prestar(self):
        for prestamo in self:
            if prestamo.state != "borrador":
                raise UserError("Solo se puede prestar un préstamo en borrador.")
            if not prestamo.linea_ids:
                raise UserError("Agregue al menos un equipo al préstamo.")
            prestamo.linea_ids.equipo_id.write({"estado": "prestado"})
            prestamo.state = "prestado"
            prestamo.message_post(
                body=f"Se prestaron {prestamo.cantidad_equipos} equipo(s) a "
                f"{prestamo.partner_id.name}."
            )

    def action_devolver(self):
        for prestamo in self:
            if prestamo.state not in ("prestado", "atrasado"):
                raise UserError("Solo se puede devolver un préstamo activo.")
            prestamo.linea_ids.equipo_id.write({"estado": "disponible"})
            prestamo.state = "devuelto"
            prestamo.message_post(body="Los equipos fueron devueltos.")
