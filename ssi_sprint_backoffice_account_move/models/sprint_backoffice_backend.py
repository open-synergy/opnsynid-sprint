# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class SprintBackofficeBackend(models.Model):
    _inherit = "sprint_backoffice_backend"

    # API
    # NOTES:
    # up = Update Payment
    # cp = Cancel Payment
    # pi = Print Invoice
    api_invoice_up = fields.Char(
        string="Update Payment",
    )
    api_invoice_cp = fields.Char(
        string="Cancel Payment",
    )
    api_invoice_pi = fields.Char(
        string="Print Invoice",
    )

    # CONFIGURATION
    pph_23_account_ids = fields.Many2many(
        string="PPh 23 Accounts",
        comodel_name="account.account",
        relation="rel_company_2_pph_23_account",
        column1="company_id",
        column2="account_id",
    )
