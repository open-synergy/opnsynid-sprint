# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from datetime import datetime

from openerp import api, fields, models


class CreateEmaterai(models.TransientModel):
    _name = "sprint.create.ematerai"
    _description = "Create E-Materai Document"

    @api.model
    def _compute_allowed_ematerai_type_ids(self):
        model_name = self.env.context.get("active_model", False)
        obj_ematerai_type = self.env["sprint.ematerai_type"]
        obj_model = self.env["ir.model"]

        model_id = False
        result = []

        if model_name:
            obj_model = self.env["ir.model"]
            criteria = [
                ("model", "=", model_name),
            ]
            models = obj_model.search(criteria)
            if len(models) > 0:
                model_id = models[0]
        if model_id:
            criteria = [("model_id", "=", model_id.id)]
            result = obj_ematerai_type.search(criteria).ids
        return result

    allowed_ematerai_type_ids = fields.Many2many(
        string="Allowed Ematerai Type",
        comodel_name="sprint.ematerai_type",
        default=lambda self: self._compute_allowed_ematerai_type_ids(),
        relation="rel_create_sprint_ematerai_2_type",
        column1="wizard_id",
        column2="ematerai_type_id",
    )
    ematerai_type_id = fields.Many2one(
        string="E-Materai Type",
        comodel_name="sprint.ematerai_type",
        required=True,
    )

    @api.multi
    def action_create(self):
        for record in self:
            record._action_create()

    @api.multi
    def _prepare_ematerai_data(self):
        self.ensure_one()
        model_name = self.env.context.get("active_model", False)
        active_id = self.env.context.get("active_id", False)
        original_attachment_id = self._get_report_attachment()
        return {
            "model": model_name,
            "res_id": active_id,
            "type_id": self.ematerai_type_id.id,
            "original_attachment_id": original_attachment_id.id,
        }

    @api.multi
    def _prepare_attachment_data(self, report_id):
        self.ensure_one()
        active_ids = self.env.context.get("active_ids", False)
        active_model = self.env.context.get("active_model", "")
        obj_report = self.env["ir.actions.report.xml"]
        pdf = obj_report.render_report([14], report_id.report_name, {})

        b64_pdf = base64.b64encode(pdf[0])
        datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "report_" + datetime_now
        return {
            "name": filename,
            "type": "binary",
            "datas": b64_pdf,
            "datas_fname": filename + ".pdf",
            "store_fname": filename,
            "res_model": active_model,
            "res_id": active_ids[0],
        }

    @api.multi
    def _action_create(self):
        self.ensure_one()
        obj_ematerai_document = self.env["sprint.ematerai"]
        data = self._prepare_ematerai_data()
        if data:
            obj_ematerai_document.create(data)

    @api.multi
    def _get_report_attachment(self):
        self.ensure_one()
        obj_ir_attachment = self.env["ir.attachment"]
        report_id = self.ematerai_type_id.report_id

        result = obj_ir_attachment.create(self._prepare_attachment_data(report_id))
        return result
