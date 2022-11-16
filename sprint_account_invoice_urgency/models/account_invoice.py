# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    urgent = fields.Boolean(
        string="Urgent",
        default=False,
    )
    urgency_note = fields.Text(
        string="Urgency Note",
    )

    @api.onchange(
        "urgent",
    )
    def onchange_urgency_note(self):
        if not self.urgent:
            self.urgency_note = ""
