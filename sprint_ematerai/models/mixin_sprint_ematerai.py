# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, fields, models


class MixinSprintEmaterai(models.AbstractModel):
    _name = "mixin.sprint.ematerai"
    _description = "Mixin for Ematerai Document"

    sprint_ematerai_ids = fields.One2many(
        string="E-Materai Document(s)",
        comodel_name="sprint.ematerai",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )

    @api.multi
    def unlink(self):
        sprint_ematerai_ids = self.mapped("sprint_ematerai_ids")
        res = super(MixinSprintEmaterai, self).unlink()
        if res:
            sprint_ematerai_ids.unlink()
        return res
