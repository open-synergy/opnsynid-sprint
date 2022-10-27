# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from openerp import api, fields, models


class SprintEmateraiType(models.Model):
    _name = "sprint.ematerai_type"
    _description = "E-Materai Type"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    model_id = fields.Many2one(
        string="Referenced Model",
        comodel_name="ir.model",
        required=True,
        ondelete="restrict",
    )
    model = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )

    @api.depends(
        "model_id",
        "model",
    )
    def _compute_allowed_report_ids(self):
        obj_ir_actions_report = self.env["ir.actions.report.xml"]

        for document in self:
            result = []
            criteria = [("model", "=", document.model)]
            report_ids = obj_ir_actions_report.search(criteria)
            if report_ids:
                result = report_ids.ids
            document.allowed_report_ids = result

    allowed_report_ids = fields.Many2many(
        string="Allowed Reports",
        comodel_name="ir.actions.report.xml",
        compute="_compute_allowed_report_ids",
        store=False,
    )
    report_id = fields.Many2one(
        string="Report",
        comodel_name="ir.actions.report.xml",
        required=True,
        ondelete="restrict",
    )
    ematerai_name = fields.Char(
        string="E-Materai Name",
        required=True,
    )
    keyword = fields.Char(
        string="Keyword",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
