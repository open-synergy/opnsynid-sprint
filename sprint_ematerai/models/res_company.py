# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"
    _name = "res.company"

    # GENERAL
    sp_ematerai_base_url = fields.Char(
        string="Base URL",
    )

    # SINGLE
    sp_ematerai_username = fields.Char(
        string="Username",
    )
    sp_ematerai_password = fields.Char(
        string="Password",
    )
    sp_ematerai_token = fields.Char(
        string="Token",
    )
    sp_ematerai_api_token = fields.Char(
        string="API Token",
    )
    sp_ematerai_download = fields.Char(
        string="API E-Materai",
    )
    sp_timeout = fields.Float(
        string="Timeout",
        default=30.0,
    )

    # BATCH
    sp_batch_username = fields.Char(
        string="Username",
    )
    sp_batch_password = fields.Char(
        string="Password",
    )
    sp_batch_token = fields.Char(
        string="Token",
    )
    sp_batch_api_token = fields.Char(
        string="API Token",
    )
    sp_ematerai_batch = fields.Char(
        string="API E-Materai",
    )
    sp_batch_timeout = fields.Float(
        string="Timeout",
        default=100.0,
    )
