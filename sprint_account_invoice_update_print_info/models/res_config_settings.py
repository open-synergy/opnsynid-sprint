# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class SprintBackOfficeSettings(models.TransientModel):
    _inherit = "sprint.backoffice_config_setting"

    sp_print_invoice = fields.Char(
        string="Print Invoice",
        related="company_id.sp_print_invoice",
    )
