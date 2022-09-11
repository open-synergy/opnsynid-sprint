# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import time
import uuid
from datetime import datetime
from wsgiref.handlers import format_date_time

from openerp import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"
    _name = "res.company"

    klikpajak_client_id = fields.Char(
        string="Klikpajak Client ID",
    )
    klikpajak_client_secret = fields.Char(
        string="Klikpajak Client Secret",
    )
    klikpajak_base_url = fields.Char(
        string="Klikpajak Base URL",
    )
    klikpajak_sale_invoice_url = fields.Char(
        string="Klikpajak Sale Invoice URL",
    )
    klik_pajak_exclude_product_ids = fields.Many2many(
        string="Klikpajak Exclude Product",
        comodel_name="product.product",
        relation="rel_company_2_klikpajak_product",
        column1="company_id",
        column2="product_id",
    )

    @api.multi
    def _get_klikpajak_sale_invoice_params(self):
        self.ensure_one()
        return {
            "auto_approval": "true",
            "auto_calculate": "true",
        }

    @api.multi
    def _get_klikpajak_header(self):
        self.ensure_one()
        return {
            "Date": self._get_klikpajak_date_header(),
            "X-Idempotency-Key": str(uuid.uuid4()),
        }

    @api.multi
    def _get_klikpajak_date_header(self):
        self.ensure_one()
        now_timestamp = time.mktime(datetime.utcnow().timetuple())
        return format_date_time(now_timestamp)

    @api.multi
    def _get_klikpajak_authorization_header(self, signature):
        self.ensure_one()
        result = 'hmac username="%s",' % self.klikpajak_client_id
        result += ' algorithm="hmac-sha256",'
        result += ' headers="date request-line",'
        result += ' signature="%s"' % (signature)
        return result

    @api.multi
    def _get_klikpajak_signature_header(self, api_url, method):
        self.ensure_one()
        request_line = method + " " + api_url + " HTTP/1.1"
        now_timestamp = time.mktime(datetime.utcnow().timetuple())
        date_string = format_date_time(now_timestamp)
        payload_tupple = ("date: " + date_string, request_line)
        payload = "\n".join(payload_tupple)
        return payload
