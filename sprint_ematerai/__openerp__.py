# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sprint E-Materai Integration",
    "version": "8.0.1.0.1",
    "license": "AGPL-3",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "views/sprint_ematerai_type_views.xml",
        "views/sprint_ematerai_config_setting_views.xml",
        "views/sprint_ematerai_views.xml",
        "wizards/create_ematerai_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
