import unittest
from decimal import Decimal
from hospital_scams import amount, find_charges
import argparse

class ComparisonTests(unittest.TestCase):
    def test_multiple_rows_are_preserved(self):
        rows = [{'CPT/HCPCS CODE': '99213', 'HOSPITAL SYSTEM CHARGE CODE': str(i), 'CHARGE DESCRIPTION': 'visit', 'NSM LOCATION (Unit Price) [IP/OP]': price} for i, price in [(1, 159), (2, 1138)]]
        matches = find_charges({'Gross Charges': rows}, '99213')
        self.assertEqual([x.unit for x in matches], [Decimal('159'), Decimal('1138')])
        self.assertEqual(find_charges({'Gross Charges': rows}, 'missing'), [])
    def test_amount_rejects_bad_input(self):
        for value in ('-1', 'NaN', 'abc'):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError): amount(value)
        self.assertEqual(amount('12.50'), Decimal('12.50'))

if __name__ == '__main__': unittest.main()
