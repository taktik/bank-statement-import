# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014-2015 Therp BV <http://therp.nl>.
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

"""Implement BankStatementParser for MT940 IBAN BNP
Paribas Fortis Luxembourg files."""

import re
import logging

from openerp.addons.bank_statement_parse_mt940.mt940 import (
    MT940, str2amount, get_subfields, handle_common_subfields)

_logger = logging.getLogger(__name__)


class MT940Parser(MT940):
    """Parser for BNP Parisbas Fortis Luxembourg MT940
    bank statement import files."""

    tag_61_regex = re.compile(
        r'^(?P<date>\d{6})'
        r'(?P<line_date>\d{0,4})'
        r'(?P<sign>R?[DC])'
        r'(?P<currency>[R])'
        r'(?P<amount>\d{1,12},\d{2})'
        r'(?P<opcode>[SN]\w{3})'
        r'(?P<reference>.{16})'
    )

    def __init__(self):
        """Initialize parser - override at least header_regex."""
        super(MT940Parser, self).__init__()
        self.header_regex = "^:20:BGLMT940"
        self.header_lines = 1
        self.mt940_type = 'BNP Parisbas Fortis Luxembourg'

    def handle_tag_25(self, data):
        self.current_statement.local_account = data.split('/')[1]

    def handle_tag_28C(self, data):
        self.current_statement.statement_id = data.split("/")[0]

    def handle_tag_61(self, data):
        """get transaction values"""
        super(MT940Parser, self).handle_tag_61(data)
        re_61 = self.tag_61_regex.match(data)
        if not re_61:
            raise ValueError("Cannot parse %s" % data)
        parsed_data = re_61.groupdict()
        sign = parsed_data['sign']
        if sign in ('C', 'RD'):
            sign = 'C'
        else:
            sign = 'D'
        self.current_transaction.transferred_amount = (
            str2amount(sign, parsed_data['amount']))
        self.current_transaction.eref = parsed_data['reference']

    def handle_tag_86(self, data):
        """Parse 86 tag containing reference data."""
        if not self.current_transaction:
            return
        note = []
        data = re.split(r'(\?\d{2})', data)
        for i in xrange(1, len(data), 2):
            code = data[i]
            value = data[i + 1]
            note.append('%s %s' % (code[1:], value))
        self.current_transaction.note = '\n'.join(note)
        # Prevent handling tag 86 later for non transaction details:
        self.current_transaction = None
