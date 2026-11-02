"""Explore a hospital's published historical charges; no patient data is stored."""
import argparse
import json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

SOURCE = 'https://www.providence.org/-/media/project/psjh/shared/files/pricing/phs/json/81-4791043_santa-rosa-memorial-hospital_standardcharges.json'

@dataclass
class Charge:
    code: str
    item: str
    description: str
    unit: Decimal
    base: Decimal
    kind: str


def find_charges(data, code):
    """Keep separate rows: the same billing code may describe different services."""
    matches = []
    for section, kind, unit, base in [
        ('Gross Charges', 'Gross', 'NSM LOCATION (Unit Price) [IP/OP]', 'NSM LOCATION (Base Price) [IP/OP]'),
        ('Discount Cash Price - Gross', 'Discounted cash', 'NSM LOCATION (UNIT PRICE) DISCOUNT CASH PRICE', 'NSM LOCATION (BASE PRICE) DISCOUNT CASH PRICE'),
    ]:
        for row in data.get(section, []):
            if str(row.get('CPT/HCPCS CODE', '')).strip().upper() == code.strip().upper():
                matches.append(Charge(code, row.get('HOSPITAL SYSTEM CHARGE CODE', ''), row.get('CHARGE DESCRIPTION', ''), Decimal(str(row.get(unit, 0))), Decimal(str(row.get(base, 0))), kind))
    return matches


def amount(value):
    try:
        result = Decimal(value)
        if not result.is_finite() or result < 0:
            raise ValueError
        return result
    except (InvalidOperation, ValueError):
        raise argparse.ArgumentTypeError('Enter a nonnegative amount, such as 250.00.')


def main():
    parser = argparse.ArgumentParser(description='Compare a line-item charge with historical hospital prices.')
    parser.add_argument('--file', type=Path, default=Path('data/santa-rosa-2022.json'), help='Path to the downloaded hospital JSON file')
    parser.add_argument('--code', required=True, help='Exact CPT/HCPCS code')
    parser.add_argument('--billed', required=True, type=amount, help='Billed amount for one unit')
    args = parser.parse_args()
    try:
        with args.file.open(encoding='utf-8') as f:
            data = json.load(f, parse_float=Decimal)
        if not isinstance(data, dict) or 'Gross Charges' not in data:
            raise ValueError('This is not the supported Santa Rosa hospital file.')
        matches = find_charges(data, args.code)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f'Could not read hospital file: {exc}\nSee README for download instructions.\n')
    print('Santa Rosa Memorial Hospital | Published effective 2022-01-01 | HISTORICAL')
    print('Source:', SOURCE)
    print('Prices are per unit or base, not a bill total. Verify the service and date.\n')
    if not matches:
        print('No matching code found in the gross or discounted-cash sections. This does not mean no price exists.')
        return
    for charge in matches:
        print(f'{charge.item} | {charge.description} | {charge.kind}')
        for label, price in [('unit', charge.unit), ('base', charge.base)]:
            if price:
                print(f'  {label}: ${price:.2f} | billed minus {label}: ${args.billed-price:.2f}')
        if not charge.unit and not charge.base:
            print('  Published prices are zero; verify the source before comparing.')
    print('\nA difference does not establish an error or fraud. Verify quantity, setting, date, insurance and exact service with the hospital.')

if __name__ == '__main__':
    main()
