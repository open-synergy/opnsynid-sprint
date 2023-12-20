# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class AccountMoveUpdatePrintInfo(models.Model):
    _name = "account_move_update_print_info"

    move_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.move",
    )
    date = fields.Datetime(
        string="Date",
        default=fields.Datetime.now(),
    )
    source = fields.Char(
        string="Source",
    )
    status_code = fields.Char(
        string="Status Code",
    )
    status_msg = fields.Char(
        string="Status",
    )
