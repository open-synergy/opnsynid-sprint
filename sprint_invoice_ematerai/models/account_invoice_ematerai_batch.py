# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class AccountInvoiceEmateraiBatch(models.Model):
    _name = "account.invoice_ematerai_batch"
    _inherit = [
        "sprint.ematerai_batch",
    ]
    _field_record = "invoice_ids"

    invoice_ids = fields.Many2many(
        string="Invoices",
        comodel_name="account.invoice",
        relation="rel_batch_2_invoice",
        column1="batch_id",
        column2="invoice_id",
        ondelete="restrict",
        required=True,
        readonly=True,
        domain="[('state', 'in', ['open','proforma','proforma2'])]",
        states={
            "draft": [("readonly", False)],
        },
    )
