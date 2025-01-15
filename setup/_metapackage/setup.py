import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-sprint",
    description="Meta package for open-synergy-opnsynid-sprint Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_sprint_backoffice',
        'odoo14-addon-ssi_sprint_backoffice_account_move',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
