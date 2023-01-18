# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class SprintBackOfficeSettings(models.TransientModel):
    _name = "sprint.backoffice_config_setting"
    _inherit = ["res.config.settings"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    sp_backoffice_url = fields.Char(
        string="Base URL",
        related="company_id.sp_backoffice_url",
    )
