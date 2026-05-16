import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-attendance-revision",
    description="Meta package for open-synergy-ssi-attendance-revision Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_attendance_revision_operating_unit',
        'odoo14-addon-ssi_attendance_revission',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
