# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
    cancel_payment_history_ids = fields.One2many(
        string="Cancel Payment History",
        comodel_name="account.invoice_cancel_payment_history",
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
            "pph23": 0.0,
            "pay_date": self.last_payment_date,
            "note": self.comment,
            "selisih": self.residual,
        }

    @api.multi
    def _prepare_cancel_payment_data(self):
        self.ensure_one()
        return {
            "id": self.id,
            "no_invoice": self.internal_number,
            "total": self.amount_total,
            "payment": (self.amount_total - self.residual),
            "pph23": 0.0,
            "pay_date": self.last_payment_date,
            "note": self.comment,
            "selisih": self.residual,
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
    def _prepare_cancel_payment_history_data(self, code, msg, src):
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
        response = None
        obj_history = self.env["account.invoice_update_payment_history"]
        base_url = self.company_id.sp_backoffice_url
        url = base_url + self.company_id.sp_update_payment
        params = self._prepare_update_payment_data()
        headers = {}

        try:
            response = requests.request("POST", url, headers=headers, params=params)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            resp_code = "TO"
            resp_message = msg_err
        except HTTPError as e:
            resp_code = response.status_code
            resp_message = e.response.text
        except BaseException as err:
            msg_err = _("%s") % (err)
            resp_code = "BaseException"
            resp_message = msg_err

        if response:
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
    def _cancel_payment(self, src):
        self.ensure_one()
        response = None
        obj_history = self.env["account.invoice_cancel_payment_history"]
        base_url = self.company_id.sp_backoffice_url
        url = base_url + self.company_id.sp_cancel_payment
        params = self._prepare_cancel_payment_data()
        headers = {}

        try:
            response = requests.request("POST", url, headers=headers, params=params)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            resp_code = "TO"
            resp_message = msg_err
        except HTTPError as e:
            resp_code = response.status_code
            resp_message = e.response.text
        except BaseException as err:
            msg_err = _("%s") % (err)
            resp_code = "BaseException"
            resp_message = msg_err

        if response:
            if response.status_code == 200:
                result = response.json()
                resp_code = result["code"]
                resp_message = result["message"]
            else:
                resp_code = response.status_code
                resp_message = response.reason

        obj_history.create(
            self._prepare_cancel_payment_history_data(resp_code, resp_message, src)
        )

    @api.multi
    def action_number(self):
        _super = super(AccountInvoice, self)
        res = _super.action_number()
        for document in self:
            document._update_payment("Invoice Validation")
        return res

    @api.multi
    def action_manual_update_payment(self):
        for document in self:
            document._update_payment("Manual Update")

    @api.multi
    def action_manual_cancel_payment(self):
        for document in self:
            document._cancel_payment("Manual Update")
