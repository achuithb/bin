#!/usr/bin/python

import argparse
import os
import re
import sys

import utils


class EtradeParser(object):

  ETRADE_DIR = os.path.join(utils.HOME_DIR, 'Documents', 'etrade')
  ETRADE_FILE = os.path.join(ETRADE_DIR, 'etrade_{year}.txt')
  DEFAULT_YEAR = 2019
  CATEGORY_FILE = 'etrade_categories.txt'
  OVERRIDE_CATEGORY_FILE = 'etrade_categories_{year}.txt'


  def __init__(self, etrade_file, year):
    self.parsed_results = {}
    self.etrade_file = etrade_file.format(year=year)
    self.etrade_filelen = 0
    self.beg_balance = 0
    self.end_balance = 0
    self.categories = self.InitCategories(year)

  @staticmethod
  def EmptyResult():
    return {'count': 0, 'total': 0}

  @staticmethod
  def FromDollar(v):
    return float(v.replace(',',''))

  @staticmethod
  def ToDollar(v):
    sign = ''
    if v < 0:
      sign = '-'
      v = -v
    return sign + '${:,}'.format(int(v))

  @classmethod
  def Strip(cls, v):
    if isinstance(v, list):
      return [cls.Strip(e) for e in v]
    else:
      return v.strip("' \n")

  @staticmethod
  def SearchExpression():
    non_tab = r'([^\t]+)'
    opt_non_tab = r'([^\t]*)'
    tab = r'\t'
    return (r'^' + non_tab + tab + opt_non_tab + tab +
            non_tab + tab + non_tab + tab + non_tab + r'$')

  @classmethod
  def InitCategories(cls, year):
    categories = {}

    current_dir = os.path.dirname(__file__)
    category_path = os.path.join(current_dir, cls.CATEGORY_FILE)
    if not os.path.isfile(category_path):
      category_path = os.path.join(cls.ETRADE_DIR, cls.CATEGORY_FILE)
    if not os.path.isfile(category_path):
      raise Exception('Could not find category file.')

    cat_set = set(open(category_path).readlines())

    override_category_filename = cls.OVERRIDE_CATEGORY_FILE.format(year=year)
    override_category_path = os.path.join(current_dir,
                                          override_category_filename)
    if not os.path.isfile(override_category_path):
      override_category_path = os.path.join(cls.ETRADE_DIR,
                                            override_category_filename)
    if os.path.isfile(override_category_path):
      cat_set.update(open(override_category_path).readlines())

    for c in cat_set:
      key, value = c.split(':')
      values = value.split(',')
      categories[cls.Strip(key)] = cls.Strip(value.split(','))
    # print(categories)
    return categories

  def ProcessMatch(self, m):
    if m.group(1) == 'Date':
      return

    # print(m.string.rstrip())
    description = m.group(2) or m.group(3)
    amount = self.FromDollar(m.group(4))
    balance = self.FromDollar(m.group(5))
    if not self.end_balance:
      self.end_balance = balance
    self.beg_balance = balance

    found = False
    for category in self.parsed_results.keys():
      if re.search(category, description):
        d = self.parsed_results[category]
        d['count'] += 1
        d['total'] += amount
        found = True
        break
    if not found:
      raise Exception('Unknown description: %s' % description)

  def Search(self):
    self.parsed_results = {key: self.EmptyResult() for key in self.categories.keys()}
    with open(self.etrade_file, 'r') as f:
      self.etrade_filelen = 0
      search_exp = self.SearchExpression()
      for line in f:
        self.etrade_filelen += 1
        m = re.search(search_exp, line)
        if not m:
          raise Exception('Failed to parse: %s' % line)
        self.ProcessMatch(m)

  def Process(self):
    entries = 0
    results = {}
    composite_results = {}
    # print(self.parsed_results)
    for key in self.parsed_results.keys():
      d = self.parsed_results[key]
      count = d['count']
      total = d['total']
      entries += count
      for i in range(len(self.categories[key])):
        name = self.categories[key][i]
        res = results if i == 0 else composite_results
        if not res.has_key(name):
          res[name] = self.EmptyResult()
        res[name]['count'] += count
        res[name]['total'] += total

    self.Print(results, composite_results)
    return entries

  @classmethod
  def PrintResults(cls, color, results):
    for key in sorted(results.keys()):
      utils.ColorPrint(color, '%s (instances %d): %s' %
                       (key, results[key]['count'],
                        cls.ToDollar(results[key]['total'])))

  def Print(self, results, composite_results):
    utils.ColorPrint(utils.GREEN,
                     'Beginning Balance: %s' % self.ToDollar(self.beg_balance))
    utils.ColorPrint(utils.GREEN,
                     'Ending Balance: %s' % self.ToDollar(self.end_balance))
    utils.ColorPrint(
        utils.GREEN, 'Difference: %s' %
        self.ToDollar(self.end_balance - self.beg_balance))
    print('')
    self.PrintResults(utils.BLACK, results)
    print('')
    self.PrintResults(utils.BLUE, composite_results)

  def Verify(self, entries):
    if (self.etrade_filelen - entries) != 1:
      raise Exception('Unexpected entries: filelen=%d, entries=%d'
                      % (filelen, entries))

  def Run(self):
    self.Search()
    entries = self.Process()
    self.Verify(entries)

  @classmethod
  def ParseArgs(cls, argv):
    parser = argparse.ArgumentParser('Parse Etrade bank statements')
    parser.add_argument('--year', default=cls.DEFAULT_YEAR,
                        help='default %s' % cls.DEFAULT_YEAR)
    parser.add_argument('--file', default=cls.ETRADE_FILE,
                        help='default %s' % cls.ETRADE_FILE)
    return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = EtradeParser.ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)

  EtradeParser(opts.file, opts.year).Run()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
