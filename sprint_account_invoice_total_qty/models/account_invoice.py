# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import openerp.addons.decimal_precision as dp
from openerp import api, fields, models


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    @api.multi
    @api.depends(
        "invoice_line.quantity",
    )
    def _compute_total_qty(self):
        for document in self:
            document.total_qty = sum(line.quantity for line in document.invoice_line)

    total_qty = fields.Float(
        string="Total Qty",
        digits=dp.get_precision("Product Unit of Measure"),
        store=True,
        readonly=True,
        compute="_compute_total_qty",
    )
