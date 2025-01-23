# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import requests
from requests.exceptions import HTTPError

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = [
        "account.move",
        "sprint_backoffice_mixin",
    ]

    customer_code = fields.Char(
        string="Customer Code",
    )
    email_cc = fields.Char(
        string="CC",
    )
    urgent = fields.Boolean(
        string="Urgent",
        default=False,
    )
    urgency_note = fields.Text(
        string="Urgency Note",
    )
    update_payment_history_ids = fields.One2many(
        string="Update Payment History",
        comodel_name="account_move_update_payment_history",
        inverse_name="move_id",
        readonly=True,
    )
    cancel_payment_history_ids = fields.One2many(
        string="Cancel Payment History",
        comodel_name="account_move_cancel_payment_history",
        inverse_name="move_id",
        readonly=True,
    )
    update_print_info_ids = fields.One2many(
        string="Update Print Info History",
        comodel_name="account_move_update_print_info",
        inverse_name="move_id",
        readonly=True,
    )

    @api.onchange(
        "urgent",
    )
    def onchange_urgency_note(self):
        if not self.urgent:
            self.urgency_note = ""

    # UPDATE PAYMENT
    def _get_pph_23_amount(self):
        self.ensure_one()
        result = 0.0
        backend = self.sprint_backoffice_backend_id
        accounts = backend.pph_23_account_ids
        for payment in self.move_line_payment_ids:
            for line in payment.move_id.line_ids:
                if line.account_id.id in accounts.ids:
                    result += line.debit
        return result

    def _prepare_update_payment_data(self):
        self.ensure_one()
        xmlid = self.export_data(['id']).get('datas')[0][0] 
        return {
            "id": xmlid,
            "no_invoice": self.name,
            "total": self.amount_total,
            "payment": (self.amount_total - self.amount_residual),
            "pph23": self._get_pph_23_amount(),
            "pay_date": self.last_payment_date,
            "note": self.narration,
            "selisih": self.amount_residual,
        }

    def _prepare_update_payment_history_data(self, code, msg, src):
        self.ensure_one()
        return {
            "move_id": self.id,
            "date": fields.Datetime.now(),
            "source": src,
            "status_code": code,
            "status_msg": msg,
        }

    def _update_payment(self, src, **kwargs):
        self.ensure_one()
        response = None
        headers = {}
        resp_code = ""
        resp_message = ""
        obj_history = self.env["account_move_update_payment_history"]
        backend = self.sprint_backoffice_backend_id
        base_url = backend.base_url
        url = base_url + backend.api_invoice_up
        params = self._prepare_update_payment_data()
        if kwargs:
            for key, value in kwargs.items():
                if key in params:
                    params[key] = value

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

    def action_manual_update_payment(self):
        for document in self:
            description = "Manual update payment for %s" % (document.name)
            document.with_delay(description=_(description))._update_payment("Manual")

    # CANCEL PAYMENT
    def _prepare_cancel_payment_history_data(self, code, msg, src):
        self.ensure_one()
        return {
            "move_id": self.id,
            "date": fields.Datetime.now(),
            "source": src,
            "status_code": code,
            "status_msg": msg,
        }

    def _prepare_cancel_payment_data(self):
        self.ensure_one()
        xmlid = self.export_data(['id']).get('datas')[0][0]
        return {
            "id": xmlid,
            "no_invoice": self.name,
            "total": self.amount_total,
            "payment": (self.amount_total - self.amount_residual),
            "pph23": self._get_pph_23_amount(),
            "pay_date": self.last_payment_date,
            "note": self.narration,
            "selisih": self.amount_residual,
        }

    def _cancel_payment(self, src, **kwargs):
        self.ensure_one()
        response = None
        headers = {}
        obj_history = self.env["account_move_cancel_payment_history"]
        resp_code = ""
        resp_message = ""
        backend = self.sprint_backoffice_backend_id
        base_url = backend.base_url
        url = base_url + backend.api_invoice_cp
        params = self._prepare_cancel_payment_data()
        if kwargs:
            for key, value in kwargs.items():
                if key in params:
                    params[key] = value

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

    def action_manual_cancel_payment(self):
        for document in self:
            description = "Manual cancel payment for %s" % (document.name)
            document.with_delay(description=_(description))._cancel_payment("Manual")

    def button_cancel(self):
        _super = super(AccountMove, self)
        res = _super.button_cancel()
        for document in self:
            if document.move_type == "out_invoice":
                description = "Cancel payment for %s" % (document.name)
                src = "Invoice Cancellation"
                document.with_delay(description=_(description))._cancel_payment(src)
        return res

    # UPDATE PRINT INFO
    def _prepare_update_print_info(self):
        self.ensure_one()
        xmlid = self.export_data(['id']).get('datas')[0][0]
        return {
            "id": xmlid,
            "no_inv": self.name,
            "print_date": self.invoice_date,
            "due_date": self.invoice_date_due,
        }

    def _prepare_update_print_info_data(self, status_code, status_msg, src):
        self.ensure_one()
        return {
            "move_id": self.id,
            "date": fields.Datetime.now(),
            "source": src,
            "status_code": status_code,
            "status_msg": status_msg,
        }

    def _update_print_info(self, src, **kwargs):
        self.ensure_one()
        response = None
        obj_history = self.env["account_move_update_print_info"]
        resp_code = ""
        resp_message = ""
        backend = self.sprint_backoffice_backend_id
        base_url = backend.base_url
        url = base_url + backend.api_invoice_pi
        headers = {}
        params = self._prepare_update_print_info()
        if kwargs:
            for key, value in kwargs.items():
                if key in params:
                    params[key] = value

        try:
            response = requests.request("POST", url, headers=headers, params=params)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            resp_code = "Timeout"
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
            self._prepare_update_print_info_data(resp_code, resp_message, src)
        )

    def action_manual_update_print_info(self):
        for document in self:
            description = "Manual update print info for %s" % (document.name)
            document.with_delay(description=_(description))._update_print_info("Manual")

    # ACCOUNT MOVE
    def action_post(self):
        _super = super(AccountMove, self)
        res = _super.action_post()
        for document in self:
            if document.move_type == "out_invoice":
                description = "Update payment for %s" % (document.name)
                src = "Invoice Confirmation"
                document.with_delay(description=_(description))._update_payment(src)

                description = "Update print info for %s" % (document.name)
                src = "Invoice Confirmation"
                document.with_delay(description=_(description))._update_print_info(src)
        return res
