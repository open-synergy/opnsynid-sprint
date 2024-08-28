import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-open-synergy-opnsynid-sprint",
    description="Meta package for open-synergy-opnsynid-sprint Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-sprint_account_invoice_cc',
        'odoo8-addon-sprint_account_invoice_customer_code',
        'odoo8-addon-sprint_account_invoice_last_backoffice_sync',
        'odoo8-addon-sprint_account_invoice_print_date',
        'odoo8-addon-sprint_account_invoice_total_qty',
        'odoo8-addon-sprint_account_invoice_update_print_info',
        'odoo8-addon-sprint_account_invoice_urgency',
        'odoo8-addon-sprint_back_office',
        'odoo8-addon-sprint_efaktur',
        'odoo8-addon-sprint_ematerai',
        'odoo8-addon-sprint_invoice_ematerai',
        'odoo8-addon-sprint_klikpajak',
        'odoo8-addon-sprint_product_category_code',
        'odoo8-addon-sprint_receipt_update_back_office',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 8.0',
    ]
)
