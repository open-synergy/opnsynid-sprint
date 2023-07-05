# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class KlikPajaksettings(models.TransientModel):
    _name = "account.klikpajak_config_setting"
    _inherit = ["res.config.settings"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    klikpajak_client_id = fields.Char(
        string="Klik Pajak Client ID",
        related="company_id.klikpajak_client_id",
    )
    klikpajak_client_secret = fields.Char(
        string="Klikpajak Client Secret",
        related="company_id.klikpajak_client_secret",
    )
    klikpajak_base_url = fields.Char(
        string="Klikpajak Base URL",
        related="company_id.klikpajak_base_url",
    )
    klikpajak_sale_invoice_url = fields.Char(
        string="Klikpajak Sale Invoice URL",
        related="company_id.klikpajak_sale_invoice_url",
    )
    klikpajak_cancel_sale_invoice_url = fields.Char(
        string="Klikpajak Cancel Sale Invoice URL",
        related="company_id.klikpajak_cancel_sale_invoice_url",
    )
    klik_pajak_exclude_product_ids = fields.Many2many(
        string="Klikpajak Exclude Product",
        comodel_name="product.product",
        related="company_id.klik_pajak_exclude_product_ids",
    )
