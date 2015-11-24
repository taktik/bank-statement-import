import setuptools
import setuptools_odoo

setup_keywords = setuptools_odoo.prepare('account_bank_statement_import_mt940_nl_ing')
setuptools.setup(**setup_keywords)
