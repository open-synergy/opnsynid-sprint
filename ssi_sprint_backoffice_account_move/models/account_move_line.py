# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def reconcile(self):
        _super = super(AccountMoveLine, self)
        res = _super.reconcile()
        for document in self:
            if document.move_id.move_type == "out_invoice":
                description = "Update payment for %s" % (document.name)
                src = "Invoice Payment"
                document.move_id.with_delay(description=_(description))._update_payment(
                    src
                )
        return res

    def remove_move_reconcile(self):
        _super = super(AccountMoveLine, self)
        invoices = []
        for document in self:
            invoices = document.matched_debit_ids.mapped("debit_move_id").filtered(
                lambda x: x.move_id.move_type == "out_invoice"
            )
            invoices += document.matched_credit_ids.mapped("credit_move_id").filtered(
                lambda x: x.move_id.move_type == "out_invoice"
            )
        res = _super.remove_move_reconcile()
        if invoices:
            for invoice in invoices:
                description = "Cancel payment for %s" % (invoice.name)
                src = "Invoice Payment Cancellation"
                invoice.move_id.with_delay(description=_(description))._cancel_payment(
                    src
                )
        return res
