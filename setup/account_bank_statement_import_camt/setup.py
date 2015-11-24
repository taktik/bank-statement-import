import setuptools
import setuptools_odoo

setup_keywords = setuptools_odoo.prepare('account_bank_statement_import_camt')
setuptools.setup(**setup_keywords)
