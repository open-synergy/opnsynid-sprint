# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    last_backoffice_sync = fields.Datetime(
        string="Last Backoffice Sync.",
        readonly=True,
    )
    last_tax_computation = fields.Datetime(
        string="Last Tax Computation",
        readonly=True,
    )

    @api.depends(
        "last_tax_computation",
        "last_backoffice_sync",
    )
    def _compute_need_tax_computation(self):
        for record in self:
            if not record.last_tax_computation:
                record.need_tax_computation = True
            else:
                if not record.last_backoffice_sync:
                    record.need_tax_computation = False
                elif record.last_backoffice_sync > record.last_tax_computation:
                    record.need_tax_computation = True
                else:
                    record.need_tax_computation = False

    need_tax_computation = fields.Boolean(
        string="Need Tax Computation",
        compute="_compute_need_tax_computation",
        store=True,
    )

    @api.multi
    def button_reset_taxes(self):
        _super = super(AccountInvoice, self)
        res = _super.button_reset_taxes()
        for document in self:
            document.last_tax_computation = fields.Datetime.now()

        return res
