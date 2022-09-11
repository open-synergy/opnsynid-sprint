# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=W0622

import base64
import hashlib
import hmac
import json
import logging

import requests
import urllib2
from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    klikpajak_id = fields.Integer(
        string="Klikpajak ID",
        readonly=True,
        copy=False,
    )
    klikpajak_invoice_status = fields.Selection(
        string="Klikpajak Invoice Status",
        selection=[
            ("NORMAL", "Normal"),
            ("NORMAL_SUB", "Substitution"),
            ("SUBSTITUED", "Substituted"),
            ("CANCELLED", "Cancel"),
        ],
        readonly=True,
        copy=False,
    )
    klikpajak_approval_status = fields.Selection(
        string="Klikpajak Approval Status",
        selection=[
            ("DRAFT", "Draft"),
            ("APPROVED", "Approved"),
            ("IN_PROGRESS", "In Progress"),
            ("REJECTED", "Reject"),
        ],
        readonly=True,
        copy=False,
    )
    klikpajak_cancel_status = fields.Char(
        string="Klikpajak Cancel Status",
        readonly=True,
        copy=False,
    )
    klikpajak_qrcode_link = fields.Char(
        string="Klikpajak QRCode Linke",
        readonly=True,
        copy=False,
    )
    klikpajak_invoice_link = fields.Char(
        string="Klikpajak Invoice Linke",
        readonly=True,
        copy=False,
    )

    @api.multi
    def _prepare_klikpajak_json_data(self):
        self.ensure_one()
        invoice_lines = []
        commercial_part = self.partner_id.commercial_partner_id
        customer_data = commercial_part._prepare_klikpajak_json_data()

        if self.taxform_address_id:
            customer_data["address"] = self.taxform_address_id._klikpajak_get_alamat()

        invoice_lines.append(self._prepare_klikpajak_line_json_data())

        return {
            "client_reference_id": self.number,
            "reference": self.number,
            "transaction_detail": self.transaction_type_id.code,
            "additional_trx_detail": "00",  # TODO
            "substitution_flag": self._get_substitution_flag(self.fp_state),
            "substituted_faktur_id": None,
            "document_number": self.nomor_seri_id.name,
            "document_date": self.date_taxform,
            "customer": customer_data,
            "items": invoice_lines,
            "total_price": 0,
            "total_discount": 0,
            "total_dpp": 0,
            "total_ppn": 0,
            "total_ppnbm": 0,
        }

    @api.multi
    def _prepare_klikpajak_line_json_data(self):
        self.ensure_one()
        return {
            "name": self.name,
            "unit_price": int(self._get_klikpajak_amount_untaxed()),
            "quantity": 1.0,
            "discount": 0.0,
            "ppnbm_rate": 0,
        }

    @api.multi
    def _get_klikpajak_amount_untaxed(self):
        self.ensure_one()
        result = self.amount_untaxed
        for line in self.invoice_line.filtered(lambda r: not r.invoice_line_tax_id):
            result -= line.price_subtotal

        return result

    @api.multi
    def action_klikpajak_submit_sale_invoice(self):
        for record in self:
            record._klikpajak_submit_sale_invoice()

    @api.multi
    def action_klikpajak_approve_sale_invoice(self):
        for record in self:
            record._klikpajak_approve_sale_invoice()

    @api.multi
    def action_klikpajak_redownload_pdf(self):
        for record in self:
            record._klikpajak_redownload_pdf()

    @api.multi
    def _klikpajak_redownload_pdf(self):
        self.ensure_one()
        attachment = self._get_klikpajak_pdf(self.klikpajak_invoice_link)
        if attachment:
            self._post_klikpajak_pdf(attachment)

    @api.multi
    def _get_klikpajak_pdf(self, url):
        self.ensure_one()
        url = url.replace("preview", "pdf")
        url = url.replace("public", "public/api")
        IrAttachment = self.env["ir.attachment"]
        try:
            r = urllib2.urlopen(url)
            r_read = r.read()
            # r = requests.get(url, allow_redirects=True)
            # b64_pdf = base64.b64encode(r.content)
            b64_pdf = base64.b64encode(r_read)
            filename = "efaktur_" + self.nomor_seri_id.name
            ir_values = {
                "name": filename,
                "type": "binary",
                "datas": b64_pdf,
                "datas_fname": filename + ".pdf",
                "store_fname": filename,
                "res_model": self._name,
                "res_id": self.id,
                "mimetype": "application/x-pdf",
            }
            attachment = IrAttachment.create(ir_values)
        except Exception as e:
            _logger.info(url)
            _logger.info(e)
            return False
        return attachment

    @api.multi
    def _post_klikpajak_pdf(self, attachment):
        self.ensure_one()
        message = _("E-Faktur is successfully created")
        self.message_post(
            body=message, message_type="notification", attachment_ids=[attachment.id]
        )

    @api.multi
    def _klikpajak_approve_sale_invoice(self):
        self.ensure_one()

        base_url = self.company_id.klikpajak_base_url
        api_url = base_url + "/v1/efaktur/out/" + str(self.klikpajak_id) + "/approve/"
        headers = self._get_klikpajak_sale_invoice_header(
            "/v1/efaktur/out/" + str(self.klikpajak_id) + "/approve/", "PUT"
        )

        response = requests.put(api_url, headers=headers)

        if response.status_code == 201 or response.status_code == 200:
            response_json = json.loads(response.text)
            data = response_json["data"]
            self.write(
                {
                    "klikpajak_approval_status": data["approval_status"],
                }
            )
        else:
            str_error = """Response code: {}

            {}""".format(
                response.status_code,
                response.text,
            )

            raise UserError(str_error)

    @api.multi
    def _get_substitution_flag(self, fp_state):
        self.ensure_one()
        if fp_state == "0":
            return False
        else:
            return True

    @api.multi
    def _get_signature(self, url, method):
        self.ensure_one()
        secret = self.company_id.klikpajak_client_secret

        payload = self.company_id._get_klikpajak_signature_header(url, method)
        hmac_signature = hmac.new(
            key=secret.encode("utf-8"),
            msg=payload.encode("utf-8"),
            digestmod=hashlib.sha256,
        )
        hmac_digest = hmac_signature.digest()

        signature = base64.b64encode(hmac_digest).decode("utf-8")
        return signature

    @api.multi
    def _get_klikpajak_sale_invoice_header(self, url, method):
        self.ensure_one()
        result = self.company_id._get_klikpajak_header()

        signature = self._get_signature(url, method)

        authorization = self.company_id._get_klikpajak_authorization_header(signature)
        result.update(
            {
                "Authorization": authorization,
            }
        )
        return result

    @api.multi
    def _klikpajak_submit_sale_invoice(self):
        self.ensure_one()
        base_url = self.company_id.klikpajak_base_url
        sale_invoice_url = self.company_id.klikpajak_sale_invoice_url
        api_url = base_url + sale_invoice_url
        headers = self._get_klikpajak_sale_invoice_header(sale_invoice_url, "POST")
        params = self.company_id._get_klikpajak_sale_invoice_params()
        json_data = self._prepare_klikpajak_json_data()

        response = requests.post(
            api_url, params=params, headers=headers, json=json_data
        )

        if response.status_code == 201 or response.status_code == 200:
            response_json = json.loads(response.text)
            data = response_json["data"]
            self.write(
                {
                    "klikpajak_id": data["id"],
                    "klikpajak_invoice_status": data["invoice_status"],
                    "klikpajak_approval_status": data["approval_status"],
                    "klikpajak_qrcode_link": data["qr_code"],
                    "klikpajak_invoice_link": data["tax_invoice_link"],
                }
            )
            # attachment = self._get_klikpajak_pdf(self.klikpajak_invoice_link)
            # if attachment:
            #     self._post_klikpajak_pdf(attachment)
        else:
            str_error = """Response code: {}

            {}""".format(
                response.status_code,
                response.text,
            )

            raise UserError(str_error)
