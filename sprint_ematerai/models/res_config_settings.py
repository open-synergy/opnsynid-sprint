# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class SprintEmateraiSettings(models.TransientModel):
    _name = "sprint.ematerai_config_setting"
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
    sp_ematerai_username = fields.Char(
        string="Username",
        related="company_id.sp_ematerai_username",
    )
    sp_ematerai_password = fields.Char(
        string="Password",
        related="company_id.sp_ematerai_password",
    )
    sp_ematerai_token = fields.Char(
        string="Token",
        related="company_id.sp_ematerai_token",
    )
    sp_ematerai_base_url = fields.Char(
        string="Base URL",
        related="company_id.sp_ematerai_base_url",
    )
    sp_ematerai_api_token = fields.Char(
        string="API Token",
        related="company_id.sp_ematerai_api_token",
    )
    sp_ematerai_download = fields.Char(
        string="API Download Doc.",
        related="company_id.sp_ematerai_download",
    )
