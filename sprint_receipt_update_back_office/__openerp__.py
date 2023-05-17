# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "SPRINT - Receipt Update Back Office",
    "version": "8.0.2.1.0",
    "license": "AGPL-3",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "sprint_back_office",
        "account_invoice_last_payment",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_setting_views.xml",
        "views/account_invoice_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
