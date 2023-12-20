# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _name = "res.company"
    _inherit = [
        "res.company",
    ]

    sprint_backoffice_backend_id = fields.Many2one(
        string="Active Sprint Backoffice Backend",
        comodel_name="sprint_backoffice_backend",
        domain="[('state', '=', 'running')]",
    )
