# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice E-Materai",
    "version": "8.0.2.1.0",
    "license": "LGPL-3",
    "category": "Invoicing",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "depends": [
        "account",
        "sprint_ematerai",
    ],
    "data": [
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "views/account_invoice_views.xml",
        "views/account_invoice_ematerai_batch.xml",
    ],
    "installable": True,
    "auto_install": False,
}
