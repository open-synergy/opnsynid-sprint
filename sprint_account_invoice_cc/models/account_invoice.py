# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=W0622

from openerp import fields, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    email_cc = fields.Char(
        string="CC",
    )
