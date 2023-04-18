# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=W0622,W0101

import base64
import json
import os
import tempfile
from datetime import datetime

import requests
from openerp import _, api, fields, models


class SprintEmateraiBatch(models.AbstractModel):
    _name = "sprint.ematerai_batch"
    _inherit = [
        "mail.thread",
        "base.sequence_document",
    ]
    _description = "Sprint E-Materai Batch"
    _field_record = False

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        copy=True,
    )

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        default=lambda self: self._default_user_id(),
        copy=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    date = fields.Date(
        string="Date",
        readonly=True,
        required=True,
        states={
            "draft": [("readonly", False)],
        },
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    type_id = fields.Many2one(
        string="E-Materai Type",
        comodel_name="sprint.ematerai_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    ematerai_ids = fields.One2many(
        string="Ematerai(s)",
        comodel_name="sprint.ematerai",
        inverse_name="batch_id",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for generated"),
            ("generate", "Generated"),
        ],
        default="draft",
        copy=False,
    )
    note = fields.Text(
        string="Note",
        copy=True,
    )
    response_msg = fields.Text(
        string="Response",
        copy=True,
    )

    @api.multi
    def action_generate(self):
        for document in self:
            data = document._prepare_generate_data()
            if document._get_token():
                document._generate_ematerai(data)

    @api.multi
    def _prepare_generate_data(self):
        self.ensure_one()
        res = []
        for ematerai in self.ematerai_ids:
            data = base64.decodestring(ematerai.original_attachment_data)

            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()

            with open(fname, "rb") as fp:
                contents = fp.read()
                filename = base64.encodestring(contents)
                fp.seek(0)

            value = {
                "name": ematerai.ref,
                "keyword": ematerai.type_id.keyword,
                "file": filename,
            }
            os.unlink(fname)
            res.append(value)
        return res

    @api.multi
    def _set_response(self, response_msg):
        self.ensure_one()
        result = False
        if response_msg:
            self.write(
                {
                    "response_msg": response_msg,
                }
            )
        else:
            self.write(
                {
                    "response_msg": "",
                }
            )
            result = True
        return result

    @api.multi
    def _get_token(self):
        self.ensure_one()
        company = self.env.user.company_id
        if not company.sp_ematerai_username:
            msg_err = _("Username Not Found")
            return self._set_response(msg_err)
        if not company.sp_ematerai_password:
            msg_err = _("Password Not Found")
            return self._set_response(msg_err)
        if not company.sp_ematerai_base_url:
            msg_err = _("Base URL Not Found")
            return self._set_response(msg_err)
        if not company.sp_ematerai_api_token:
            msg_err = _("API Token Not Found")
            return self._set_response(msg_err)

        url = company.sp_ematerai_base_url + company.sp_ematerai_api_token
        payload = json.dumps(
            {
                "username": company.sp_ematerai_username,
                "password": company.sp_ematerai_password,
            }
        )
        headers = {
            "Content-Type": "application/json",
        }
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            return self._set_response(msg_err)
        result = response.json()
        if result["statuscode"] == "00":
            company.sp_ematerai_token = result["token"]
            msg_err = False
            return self._set_response(msg_err)
        else:
            msg_err = _("%s") % (result["description"])
            return self._set_response(msg_err)

    @api.multi
    def _generate_ematerai(self, data):
        self.ensure_one()
        if not data:
            msg_err = _("Data E-Materai(s) Not Found")
            return self._set_response(msg_err)
        company = self.env.user.company_id
        if not company.sp_ematerai_base_url:
            msg_err = _("Base URL Not Found")
            return self._set_response(msg_err)
        if not company.sp_ematerai_batch:
            msg_err = _("API E-Materai Batch Not Found")
            return self._set_response(msg_err)

        url = company.sp_ematerai_base_url + company.sp_ematerai_batch
        headers = {
            "Authorization": "Bearer " + company.sp_ematerai_token,
        }
        payload = json.dumps({"document": data})
        # return self._set_response(payload)
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            return self._set_response(msg_err)
        except ValueError as e:
            msg_err = _(
                """
            Response: %s
            Error: %s
            """
                % (response.text, e)
            )
            return self._set_response(msg_err)

        if not response:
            msg_err = _("Can't retrieve response")
            return self._set_response(msg_err)

        return self._set_response(response.text)

    @api.multi
    def action_confirm(self):
        for document in self:
            document.action_create_ematerai()
            document.write(document._prepare_confirm_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update(
            {
                "ir_sequence_date": self.date,
            }
        )
        sequence = self.with_context(ctx)._create_sequence()
        return {
            "state": "confirm",
            "name": sequence,
        }

    @api.multi
    def action_create_ematerai(self):
        for record in self:
            record._action_create_ematerai()

    @api.multi
    def _prepare_ematerai_data(self, object):
        self.ensure_one()
        model_name = object._name
        active_id = object.id
        original_attachment_id = self._get_report_attachment(object)
        return {
            "model": model_name,
            "res_id": active_id,
            "type_id": self.type_id.id,
            "original_attachment_id": original_attachment_id.id,
            "batch_id": self.id,
        }

    @api.multi
    def _prepare_attachment_data(self, report_id, object):
        self.ensure_one()
        object_ids = [object.id]
        obj_report = self.env["ir.actions.report.xml"]
        ctx = {"active_model": self.type_id.model}
        pdf = obj_report.with_context(ctx).render_report(
            object_ids, report_id.report_name, {}
        )
        b64_pdf = base64.b64encode(pdf[0])
        datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "report_" + datetime_now
        return {
            "name": filename,
            "type": "binary",
            "datas": b64_pdf,
            "datas_fname": filename + ".pdf",
            "store_fname": filename,
            "res_model": self.type_id.model,
            "res_id": object_ids[0],
        }

    @api.multi
    def _action_create_ematerai(self):
        self.ensure_one()
        obj_ematerai_document = self.env["sprint.ematerai"]
        objects = getattr(self, self._field_record)
        for object in objects:
            data = self._prepare_ematerai_data(object)
            if data:
                obj_ematerai_document.create(data)

    @api.multi
    def _get_report_attachment(self, object):
        self.ensure_one()
        obj_ir_attachment = self.env["ir.attachment"]
        report_id = self.type_id.report_id

        result = obj_ir_attachment.create(
            self._prepare_attachment_data(report_id, object)
        )
        return result

    @api.multi
    def name_get(self):
        result = []
        for document in self:
            if document.name == "/":
                name = "*" + str(document.id)
            else:
                name = document.name
            result.append((document.id, name))
        return result
