# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"
    _name = "res.company"

    sp_timeout = fields.Float(
        string="Timeout",
        default=30.0,
    )
    sp_ematerai_username = fields.Char(
        string="Username",
    )
    sp_ematerai_password = fields.Char(
        string="Password",
    )
    sp_ematerai_token = fields.Char(
        string="Token",
    )
    sp_ematerai_base_url = fields.Char(
        string="Base URL",
    )
    sp_ematerai_api_token = fields.Char(
        string="API Token",
    )
    sp_ematerai_download = fields.Char(
        string="API E-Materai Single",
    )
    sp_ematerai_batch = fields.Char(
        string="API E-Materai Batch",
    )
