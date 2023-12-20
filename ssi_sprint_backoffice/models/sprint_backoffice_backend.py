# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class SprintBackofficeBackend(models.Model):
    _name = "sprint_backoffice_backend"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Sprint E-Materai Backend"
    _automatically_insert_print_button = False

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
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("running", "Running"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    # GENERAL
    base_url = fields.Char(
        string="Base URL",
        required=True,
    )

    def action_running(self):
        for record in self:
            check_running_backend_ids = self.search(
                [
                    ("state", "=", "running"),
                    ("company_id", "=", self.env.user.company_id.id),
                    ("id", "!=", record.id),
                ]
            )
            if check_running_backend_ids:
                check_running_backend_ids.write({"state": "draft"})
            record.company_id.write({"sprint_backoffice_backend_id": record.id})
            record.write({"state": "running"})

    def action_restart(self):
        for record in self:
            record.company_id.write({"sprint_backoffice_backend_id": False})
            record.write({"state": "draft"})
