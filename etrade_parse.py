#!/usr/bin/python

import argparse
import os
import sys

import utils


DEFAULT_DIR=os.path.join(utils.HOME_DIR, 'Documents', 'etrade')
FILENAME = 'etrade_{year}.txt'
SEARCH_EXP = r'^([^\t]+)[\t]+([^\t]+)[\t]([^\t]+)\t([^\t]+)$'

CATEGORIES = {
    'ATM FEE REFUND' : 'ATM Fee',
    'ATM WITHDRAWAL' : 'ATM Withdrawal',
    'DIRECT DEBIT - CHASE CREDIT CRD,AUTOPAY' : 'Credit card',
    'DIRECT DEBIT - IRS,USATAXPYMT' : 'IRS',
    'DIRECT DEBIT - MOUNTAIN BROOK,USBSNGPT' : 'Mountain Brook HOA',
    'DIRECT DEBIT - PAYPAL,INST XFER' : 'Paypal payment',
    'DIRECT DEBIT - PGANDE,WEB ONLINE' : 'PG&E',
    'DIRECT DEBIT - SANTANDER,CONSUMER' : 'Auto loan',
    'DIRECT DEBIT - VENMO,PAYMENT' : 'Venmo Payment',
    'DIRECT DEBIT - WF HOME MTG,AUTO PAY' : 'Mortgage',
    'DIRECT DEPOSIT - FRANCHISE TAX BD,CASTTAXRFD' : 'CA State Tax',
    'DIRECT DEPOSIT - GOOGLE LLC,BP SETTLE' : 'Google special',
    'DIRECT DEPOSIT - GOOGLE LLC,PAYROLL' : 'Google Payroll',
    'DIRECT DEPOSIT - SCHWAB BROKERAGE,MONEYLINK' : 'Schwab Transfer',
    'DIRECT DEPOSIT - VENMO,CASHOUT' : 'Venmo receipt',
    'FOREIGN TRANSACTION FEE' : 'ATM foreign transaction fee',
    'INTEREST' : 'Interest',
    'TRANSFER MONEY FROM BROKERAGE XXXX4406' : 'Transfer from Brokerage',
    'TRANSFER MONEY TO BROKERAGE XXXX4406' : 'Transfer to Brokerage',
}

category_result = {}

def Process(m):
  #print(m.string.rstrip())
  description = m.group(2)
  value = float(m.group(3).replace(',',''))

  global category_result
  found = False
  for category in category_result.keys():
    if description.find(category) == 0:
      ary = category_result[category]
      ary[0] += 1
      ary[1] += value
      found = True
      break
  if not found:
    raise Exception('Unknown description: %s' % description)


def Run(filename):
  global category_result
  category_result = {key: [0, 0] for key in CATEGORIES.keys()}
  utils.SearchFile(filename, search_exp=SEARCH_EXP, Process=Process)
  for key in category_result.keys():
    name = CATEGORIES[key]
    result = category_result[key]
    print('%s (instances %d): %.2f' % (name, result[0], result[1]))


def ParseArgs(argv):
  parser = argparse.ArgumentParser('Parse Etrade bank statements')
  parser.add_argument('--year')
  parser.add_argument('--dir', help='directory with bank statements '
                      ' in format %s' % FILENAME, default=DEFAULT_DIR)
  return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)

  if not opts.year:
    raise Exception('Must specify year.')

  Run(os.path.join(opts.dir, FILENAME.format(year=opts.year)))


if __name__ == '__main__':
  sys.exit(main(sys.argv))
