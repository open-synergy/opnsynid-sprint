# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json

import requests
from openerp import _, api, fields, models
from requests.exceptions import HTTPError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    update_payment_history_ids = fields.One2many(
        string="Update Payment History",
        comodel_name="account.invoice_update_payment_history",
        inverse_name="invoice_id",
        readonly=True,
    )

    @api.multi
    def _prepare_update_payment_data(self):
        self.ensure_one()
        return {
            "id": self.id,
            "no_invoice": self.internal_number,
            "total": self.amount_total,
            "payment": (self.amount_total - self.residual),
            "pph23": self.amount_tax,
            "pay_date": self.last_payment_date,
            "note": self.comment,
        }

    @api.multi
    def _prepare_update_payment_history_data(self, code, msg, src):
        self.ensure_one()
        return {
            "invoice_id": self.id,
            "date": fields.Datetime.now(),
            "source": src,
            "status_code": code,
            "status_msg": msg,
        }

    @api.multi
    def _update_payment(self, src):
        self.ensure_one()
        obj_history = self.env["account.invoice_update_payment_history"]
        base_url = self.company_id.sp_backoffice_url
        url = base_url + self.company_id.sp_update_payment
        payload = json.dumps(self._prepare_update_payment_data())
        headers = {}

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            resp_code = "TO"
            resp_message = msg_err
        except HTTPError as e:
            resp_code = response.status_code
            resp_message = e.response.text

        if response.status_code == 200:
            result = response.json()
            resp_code = result["code"]
            resp_message = result["message"]
        else:
            resp_code = response.status_code
            resp_message = response.reason

        obj_history.create(
            self._prepare_update_payment_history_data(resp_code, resp_message, src)
        )

    @api.multi
    def invoice_validate(self):
        _super = super(AccountInvoice, self)
        res = _super.invoice_validate()
        for document in self:
            document._update_payment("Validate")
        return res

    @api.multi
    def action_manual_update_payment(self):
        for document in self:
            document._update_payment("Manual Update")
