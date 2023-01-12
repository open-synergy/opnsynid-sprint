# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    last_backoffice_sync = fields.Datetime(
        string="Last Backoffice Sync.",
        readonly=True,
    )
