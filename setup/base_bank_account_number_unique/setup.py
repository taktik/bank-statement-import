import setuptools
import setuptools_odoo

setup_keywords = setuptools_odoo.prepare('base_bank_account_number_unique')
setuptools.setup(**setup_keywords)
