# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).
# pylint: disable=W0622,W0101

import base64
import json
import os
import tempfile
from datetime import datetime

import requests
from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class SprintEmaterai(models.Model):
    _name = "sprint.ematerai"
    _description = "Sprint E-Materai Document"

    model = fields.Char(
        string="Related Document Model",
        index=True,
    )
    res_id = fields.Integer(
        string="Related Document ID",
        index=True,
    )
    original_attachment_id = fields.Many2one(
        string="Attachment(Original)",
        comodel_name="ir.attachment",
    )
    original_attachment_data = fields.Binary(
        string="File Content Attachment(Original)",
        related="original_attachment_id.datas",
        store=False,
    )
    original_datas_fname = fields.Char(
        string="Filename Attachment(Original)",
        related="original_attachment_id.datas_fname",
        store=False,
    )
    ematerai_attachment_id = fields.Many2one(
        string="Attachment(E-Materai)",
        comodel_name="ir.attachment",
    )
    ematerai_attachment_data = fields.Binary(
        string="File Content Attachment(E-Materai)",
        related="ematerai_attachment_id.datas",
        store=False,
    )
    ematerai_datas_fname = fields.Char(
        string="Filename Attachment(E-Materai)",
        related="ematerai_attachment_id.datas_fname",
        store=False,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="sprint.ematerai_type",
    )
    batch_id = fields.Many2one(
        string="Batch ID",
        comodel_name="sprint.ematerai_batch",
        ondelete="restrict",
        readonly=True,
    )

    @api.multi
    @api.depends(
        "model",
        "res_id",
    )
    def _compute_get_reference(self):
        for record in self:
            obj = self.env[record.model]
            obj_id = obj.browse(record.res_id)
            if record.model != "account.invoice":
                ref = obj_id.name
            else:
                ref = obj_id.number
            record.ref = ref

    ref = fields.Char(
        string="Reference",
        compute="_compute_get_reference",
        store=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("success", "Success"),
        ],
        default="draft",
    )

    @api.multi
    def _get_model_record(self):
        self.ensure_one()
        obj = self.env[self.model]
        record = obj.browse(self.res_id)
        return record

    @api.multi
    def _get_document(self, data):
        self.ensure_one()
        obj_ir_attachment = self.env["ir.attachment"]
        datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "ematerai_" + datetime_now

        ir_values = {
            "name": self.ref,
            "type": "binary",
            "datas": data,
            "datas_fname": self.ref + ".pdf",
            "store_fname": filename,
            "res_model": self._name,
            "res_id": self.id,
        }
        attachment_id = obj_ir_attachment.create(ir_values)
        return attachment_id.id

    @api.multi
    def _prepare_download_document_data(self, data):
        self.ensure_one()
        attachment_id = self._get_document(data)
        return {
            "ematerai_attachment_id": attachment_id,
            "state": "success",
        }

    @api.multi
    def _get_token(self):
        self.ensure_one()
        company = self.env.user.company_id
        if not company.sp_ematerai_username:
            msg_err = _("Username Not Found")
            raise UserError(msg_err)
        if not company.sp_ematerai_password:
            msg_err = _("Password Not Found")
            raise UserError(msg_err)
        if not company.sp_ematerai_base_url:
            msg_err = _("Base URL Not Found")
            raise UserError(msg_err)
        if not company.sp_ematerai_api_token:
            msg_err = _("API Token Not Found")
            raise UserError(msg_err)

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
            raise UserError(msg_err)
        result = response.json()
        if result["statuscode"] == "00":
            company.sp_ematerai_token = result["token"]
        else:
            msg_err = _("%s") % (result["description"])
            raise UserError(msg_err)

    @api.multi
    def _download_doc(self):
        self.ensure_one()
        company = self.env.user.company_id
        type = self.type_id
        if not company.sp_ematerai_token:
            msg_err = _("Token Not Found")
            raise UserError(msg_err)
        if not company.sp_ematerai_base_url:
            msg_err = _("Base URL Not Found")
            raise UserError(msg_err)
        if not company.sp_ematerai_download:
            msg_err = _("API Download Doc. Not Found")
            raise UserError(msg_err)

        url = company.sp_ematerai_base_url + company.sp_ematerai_download
        headers = {
            "Authorization": "Bearer " + company.sp_ematerai_token,
        }
        data = base64.decodestring(self.original_attachment_data)

        fobj = tempfile.NamedTemporaryFile(delete=False)
        fname = fobj.name
        fobj.write(data)
        fobj.close()

        with open(fname, "rb") as fp:
            contents = fp.read()
            filename = base64.encodestring(contents)
            fp.seek(0)

        payload = json.dumps(
            {
                "name": self.ref,
                "keyword": type.keyword,
                "file": filename,
            }
        )

        try:
            response = requests.request("GET", url, headers=headers, data=payload)
        except requests.exceptions.Timeout:
            msg_err = _("Timeout: the server did not reply within 30s")
            raise UserError(msg_err)
        finally:
            os.unlink(fname)

        if not response:
            msg_err = _("Can't retrieve response")
            raise UserError(msg_err)

        if response.status_code == 200:
            try:
                result = response.json()
            except ValueError as e:
                error_message = _(
                    """
                Response: %s
                Error: %s
                """
                    % (response.text, e)
                )
                raise UserError(error_message)
            if "file" not in result:
                error_message = _(
                    """
                Message: %s
                Description: %s
                Status Code: %s
                """
                    % (result["message"], result["description"], result["statuscode"])
                )
                raise UserError(error_message)
            self.write(self._prepare_download_document_data(result["file"]))
        else:
            resp_code = response.status_code
            resp_message = response.reason
            error_message = _("%s - %s") % (resp_code, resp_message)
            raise UserError(error_message)

    @api.multi
    def _action_generate_ematerai(self):
        self.ensure_one()
        self._get_token()
        self._download_doc()
        return True

    @api.multi
    def action_generate_ematerai(self):
        for document in self:
            document._action_generate_ematerai()
