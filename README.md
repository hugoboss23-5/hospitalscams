# hospitalscams

A Python project to help people investigate hospital bills using hospital-published prices. This first version searches **Santa Rosa Memorial Hospital's 2022 historical file**. It is a starting point for investigation, not evidence of a scam or an estimate of a current bill.

## Try it

Requires Python 3.9 or later. Download the hospital's public file into `data/santa-rosa-2022.json`:

```sh
mkdir -p data
curl -L 'https://www.providence.org/-/media/project/psjh/shared/files/pricing/phs/json/81-4791043_santa-rosa-memorial-hospital_standardcharges.json' -o data/santa-rosa-2022.json
python3 hospital_scams.py --code 99213 --billed 1200
python3 -m unittest discover -s tests
```

The file is published by [Providence](https://www.providence.org/-/media/project/psjh/shared/files/pricing/phs/json/81-4791043_santa-rosa-memorial-hospital_standardcharges.json); its own summary states the prices were effective January 1, 2022. Retrieved November 2, 2026. It is historical, not a current price source. For example, code 99213 appears under multiple distinct hospital item codes. The program shows each rather than assuming one is the right match. A published unit price is not necessarily a total; zero base or unit prices are not interpreted as free care.

Gross and discounted cash prices are different; the latter generally applies to self-pay patients. A billed amount is not necessarily what an insured patient owes. Code, service, quantity, setting, date, and insurance must match before a comparison is useful. Ask the hospital for an itemized bill and clarification. A difference alone does not establish a billing error or fraud.

The file stays on your computer; the program does not send or save bill entries. It does not cover other hospitals, other file formats, negotiated prices, or all sections of this file. No matching result does not imply a service was not listed elsewhere.

## How it works

`Charge` is a class holding one published row. `find_charges` loops through two price sections and returns every exact code match. The program uses lists, strings, numbers, functions, arithmetic and input validation. `Decimal` keeps financial arithmetic precise.
