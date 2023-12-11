# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Sprint Back Office",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "base",
        "ssi_master_data_mixin",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/sprint_backoffice_backend_views.xml",
    ],
    "demo": [],
    "images": [],
}
