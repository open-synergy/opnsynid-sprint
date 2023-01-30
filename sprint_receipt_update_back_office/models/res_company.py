# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sp_update_payment = fields.Char(
        string="Update Payment",
    )
    sp_cancel_payment = fields.Char(
        string="Cancel Payment",
    )
