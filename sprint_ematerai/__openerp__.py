# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sprint E-Materai Integration",
    "version": "8.0.2.6.0",
    "license": "AGPL-3",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "base",
        "mail",
        "base_sequence_configurator",
        "base_action_rule",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "data/ir_filter_data.xml",
        "data/ir_actions_server_data.xml",
        "data/base_action_rule_data.xml",
        "views/sprint_ematerai_type_views.xml",
        "views/sprint_ematerai_config_setting_views.xml",
        "views/sprint_ematerai_views.xml",
        "views/sprint_ematerai_batch_views.xml",
        "wizards/create_ematerai_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
