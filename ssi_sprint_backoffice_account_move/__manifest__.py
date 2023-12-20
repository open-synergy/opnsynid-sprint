# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Sprint Back Office - Account Move",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_financial_accounting",
        "ssi_sprint_backoffice",
        "queue_job",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sprint_backoffice_backend_views.xml",
        "views/account_move_views.xml",
    ],
    "demo": [],
    "images": [],
}
