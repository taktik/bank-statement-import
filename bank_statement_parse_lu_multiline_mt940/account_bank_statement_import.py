# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ACSONE SA/NV <http://acsone.eu>.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

"""Parse a MT940 Luxembourg Multiline file."""

import logging

from openerp import models

from .mt940 import MT940Parser as Parser

_logger = logging.getLogger(__name__)


class AccountBankStatementImport(models.TransientModel):
    """Add parsing of mt940 files to bank statement import."""
    _inherit = 'account.bank.statement.import'

    def _parse_file(self, cr, uid, data_file, context=None):
        """Parse a MT940 Luxembourg Multiline file."""
        parser = Parser()
        try:
            _logger.debug("Try parsing with MT940 Luxembourg Multiline.")
            return parser.parse(data_file)
        except ValueError:
            # Returning super will call next candidate:
            _logger.debug("Statement file was not a "
                          "MT940 Luxembourg Multiline.",
                          exc_info=True)
            return super(AccountBankStatementImport, self)._parse_file(
                cr, uid, data_file, context=context)
