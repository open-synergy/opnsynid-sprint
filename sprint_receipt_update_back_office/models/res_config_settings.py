# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class SprintBackOfficeSettings(models.TransientModel):
    _inherit = "sprint.backoffice_config_setting"

    sp_update_payment = fields.Char(
        string="Update Payment",
        related="company_id.sp_update_payment",
    )
    sp_cancel_payment = fields.Char(
        string="Cancel Payment",
        related="company_id.sp_cancel_payment",
    )
    sp_pph_23_account_ids = fields.Many2many(
        string="PPh 23 Accounts",
        related="company_id.pph_23_account_ids",
    )
