# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class SprintBackofficeMixin(models.AbstractModel):
    _name = "sprint_backoffice_mixin"
    _description = "Mixin Object for Sprint Backoffice"

    @api.model
    def _get_sprint_backoffice_backend_id(self):
        company = self.env.company
        backend = company.sprint_backoffice_backend_id
        return backend and backend.id or False

    sprint_backoffice_backend_id = fields.Many2one(
        string="Backend",
        comodel_name="sprint_backoffice_backend",
        default=lambda self: self._get_sprint_backoffice_backend_id(),
        required=False,
    )
