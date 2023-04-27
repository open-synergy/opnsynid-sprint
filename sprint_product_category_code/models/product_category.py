# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openerp import _, api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    code = fields.Char(
        string="Code",
    )

    _sql_constraints = [
        (
            "product_category_unique_code",
            "UNIQUE (code)",
            _("The code must be unique!"),
        ),
    ]

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        res = super(ProductCategory, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        args = list(args or [])
        if name:
            criteria = ["|", ("code", operator, name), ("name", operator, name)]
            criteria = criteria + args
            category_ids = self.search(criteria, limit=limit)
            if category_ids:
                return category_ids.name_get()
        return res
