#!/usr/bin/python

import argparse
import os
import re
import sys

import utils


class EtradeParser(object):

  ETRADE_DIR = os.path.join(utils.HOME_DIR, 'Documents', 'etrade')
  ETRADE_FILE = os.path.join(ETRADE_DIR, 'etrade_{year}.txt')
  ETRADE_FILE_REGEXP = r'etrade_[\d]+.txt'
  DEFAULT_YEAR = 2019
  CATEGORY_FILE = 'etrade_categories.txt'
  CATEGORY_LIST = 'category_list.txt'
  OVERRIDE_CATEGORY_FILE = 'etrade_categories_{year}.txt'


  def __init__(self, etrade_file, year, list_known, min_amount, max_amount):
    self.year = year
    self.list_known = list_known
    self.etrade_file = etrade_file.format(year=year)
    self.etrade_filelen = 0
    self.min_amount = min_amount
    self.max_amount = max_amount
    self.beg_balance = 0
    self.end_balance = 0
    self.categories = {}
    self.results = {}
    self.category_list = []

    self.InitCategories()

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
  def Search(cls, etrade_file, ProcessMatch):
    with open(etrade_file, 'r') as f:
      filelen = 0
      search_exp = cls.SearchExpression()
      for line in f:
        filelen += 1
        m = re.search(search_exp, line)
        # if not m: raise Exception('Failed to parse: %s' % line)
        if m and m.group(1) != 'Date':
          match_str = m.string.rstrip()
          # print(match_str)
          description = m.group(2) or m.group(3)
          amount = cls.FromDollar(m.group(4))
          balance = cls.FromDollar(m.group(5))
          ProcessMatch(match_str, description, amount, balance)
      return filelen

  def InitCategories(self):
    categories = {}

    current_dir = os.path.dirname(__file__)
    category_path = os.path.join(current_dir, self.CATEGORY_FILE)
    if not os.path.isfile(category_path):
      category_path = os.path.join(self.ETRADE_DIR, self.CATEGORY_FILE)
    if not os.path.isfile(category_path):
      raise Exception('Could not find category file.')

    cat_set = set(open(category_path).readlines())

    override_category_filename = self.OVERRIDE_CATEGORY_FILE.format(
        year=self.year)
    override_category_path = os.path.join(current_dir,
                                          override_category_filename)
    if not os.path.isfile(override_category_path):
      override_category_path = os.path.join(self.ETRADE_DIR,
                                            override_category_filename)
    if os.path.isfile(override_category_path):
      cat_set.update(open(override_category_path).readlines())

    for c in cat_set:
      key, value = c.split(':')
      values = value.split(',')
      categories[self.Strip(key)] = self.Strip(value.split(','))
    # print(categories)

    self.categories = categories
    self.results = {key: self.EmptyResult() for key in self.categories.keys()}

  def CategorizeMatch(self, match_str, description, amount, balance):
    if not self.end_balance:
      self.end_balance = balance
    self.beg_balance = balance

    found = False
    for category in self.results.keys():
      if re.search(category, description):
        d = self.results[category]
        d['count'] += 1
        d['total'] += amount
        found = True
        break
    if not found:
      utils.ColorPrint(utils.RED, 'Unknown: %s' % match_str)

  def Categorize(self):
    entries = 0
    results = {}
    composite_results = {}
    # print(self.results)
    for key in self.results.keys():
      d = self.results[key]
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

  def Verify(self, filelen, entries):
    if (filelen - entries) != 1:
      raise Exception('Unexpected entries: filelen=%d, entries=%d'
                      % (filelen, entries))

  def Run(self):
    filelen = self.Search(self.etrade_file, self.CategorizeMatch)
    entries = self.Categorize()
    self.Verify(filelen, entries)

  def CreateCategories(self, match_str, description, amount, balance):
    # Skip match if it already exists.
    for exp in self.category_list:
      if re.search(exp, description):
        return
    c = self.results
    if not c.has_key(description):
      c[description] = self.EmptyResult()
    c[description]['count'] += 1
    c[description]['total'] += amount

  @classmethod
  def FileList(cls):
    ls = utils.RunCmd('ls %s' % cls.ETRADE_DIR, silent=True)
    return [e for e in ls.rstrip().split('\n')
            if re.search(cls.ETRADE_FILE_REGEXP, e)]

  @classmethod
  def InitCategoryList(cls):
    cat_path = os.path.join(cls.ETRADE_DIR, cls.CATEGORY_LIST)
    if os.path.isfile(cat_path):
      return [e.rstrip('\n') for e in open(cat_path).readlines()]
    return []

  def CheckAmount(self, amount):
    amount = abs(amount)
    if self.min_amount and amount < self.min_amount:
      return False
    if self.max_amount and amount > self.max_amount:
      return False
    return True

  def List(self, list_long):
    self.category_list = self.InitCategoryList()
    self.results = {key: self.EmptyResult() for key in self.category_list}
    # print '\'\n\''.join(self.category_list)
    etrade_files = self.FileList()

    ProcessMatch = (self.CategorizeMatch if self.list_known
                    else self.CreateCategories)
    for etrade_file in etrade_files:
      self.Search(os.path.join(self.ETRADE_DIR, etrade_file), ProcessMatch)

    c = self.results
    for desc in sorted(c.keys()):
      count = c[desc]['count']
      amount = c[desc]['total']
      if self.CheckAmount(amount):
        if list_long or self.list_known:
          print('%s\t%d\t%d' % (desc, count, amount))
        else:
          print(desc)

  @classmethod
  def ParseArgs(cls, argv):
    parser = argparse.ArgumentParser('Parse Etrade bank statements')
    parser.add_argument('--year', default=cls.DEFAULT_YEAR,
                        help='default %s' % cls.DEFAULT_YEAR)
    parser.add_argument('--file', default=cls.ETRADE_FILE,
                        help='default %s' % cls.ETRADE_FILE)
    parser.add_argument('--list', default=False, action='store_true',
                        help='List Unknown Descriptions')
    parser.add_argument('--list-long', default=False, action='store_true',
                        help='List Unknown Descriptions with Count and Amount')
    parser.add_argument('--list-known', default=False, action='store_true',
                        help='List Known Descriptions with Count and Amount')
    parser.add_argument('--min-amount', default=None, help='Minimum Amount')
    parser.add_argument('--max-amount', default=None, help='Maximum Amount')
    return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = EtradeParser.ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)

  etrade_parser = EtradeParser(opts.file, opts.year, opts.list_known,
                               opts.min_amount, opts.max_amount)
  if opts.list or opts.list_long or opts.list_known:
    etrade_parser.List(opts.list_long)
  else:
    etrade_parser.Run()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
