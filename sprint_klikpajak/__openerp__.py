# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sprint Klik Pajak Integration",
    "version": "8.0.1.1.0",
    "license": "AGPL-3",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "sprint_efaktur",
        "partner_company_legal_name",
    ],
    "data": [
        "views/account_klikpajak_config_setting_views.xml",
        "views/account_invoice_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
