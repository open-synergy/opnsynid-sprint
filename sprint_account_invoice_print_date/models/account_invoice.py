# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=W0622

from openerp import api, fields, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    @api.depends("manual_date_print", "date_invoice")
    def _compute_print_date(self):
        for record in self:
            result = False
            if record.manual_date_print:
                result = record.manual_date_print
            elif not record.manual_date_print and record.date_invoice:
                result = record.date_invoice

            record.date_print = result

    date_print = fields.Date(
        string="Print Date",
        compute="_compute_print_date",
        store=True,
    )
    manual_date_print = fields.Date(
        string="Manual Print Date",
    )
