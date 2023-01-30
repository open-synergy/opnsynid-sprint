# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def reconcile_partial(
        self,
        type="auto",
        writeoff_acc_id=False,
        writeoff_period_id=False,
        writeoff_journal_id=False,
        context=None,
    ):
        _super = super(AccountMoveLine, self)
        res = _super.reconcile_partial(
            type="auto",
            writeoff_acc_id=False,
            writeoff_period_id=False,
            writeoff_journal_id=False,
            context=None,
        )
        for document in self:
            if document.invoice:
                document.invoice._update_payment("Update Payment")
        return res

    @api.model
    def _remove_move_reconcile(
        self,
        move_ids=None,
        opening_reconciliation=False,
        context=None,
    ):
        _super = super(AccountMoveLine, self)
        aml_ids = self.browse(move_ids)
        invoices = self.env["account.invoice"]
        for document in aml_ids:
            reconcile = document.reconcile_id or document.reconcile_partial_id or False
            if not reconcile:
                continue

            reconcile_ids = reconcile.line_id or reconcile.line_partial_ids or False
            if not reconcile_ids:
                continue

            for recon in reconcile_ids:
                if recon.invoice:
                    invoices = recon.invoice

        res = _super._remove_move_reconcile(
            move_ids=move_ids,
            opening_reconciliation=opening_reconciliation,
            context=context,
        )

        for invoice in invoices:
            invoice._cancel_payment("Cancel Payment")

        return res
