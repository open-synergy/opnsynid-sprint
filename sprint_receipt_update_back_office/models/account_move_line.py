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
                document.invoice._update_payment("Payment Reconcile")
        return res
