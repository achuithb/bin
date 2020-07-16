#!/usr/bin/python

import argparse
import os
import sys

import utils


class EtradeParser(object):

  ETRADE_DIR = os.path.join(utils.HOME_DIR, 'Documents', 'etrade')
  ETRADE_FILE = os.path.join(ETRADE_DIR, 'etrade_{year}.txt')
  DEFAULT_YEAR = 2019
  CATEGORY_DIR = ETRADE_DIR
  CATEGORY_DIR = os.path.dirname(__file__)
  OVERRIDE_CATEGORY_FILE = os.path.join(
      CATEGORY_DIR, 'etrade_categories_{year}.txt')
  CATEGORY_FILE = os.path.join(CATEGORY_DIR, 'etrade_categories.txt')


  def __init__(self, etrade_file, year):
    self.parsed_results = {}
    self.etrade_file = etrade_file.format(year=year)
    self.categories = self.InitCategories(year)

  @classmethod
  def Strip(cls, v):
    if isinstance(v, list):
      return [cls.Strip(e) for e in v]
    else:
      return v.strip("' \n")

  @classmethod
  def InitCategories(cls, year):
    categories = {}
    cat_set = set(open(cls.CATEGORY_FILE).readlines())
    override_category_file = cls.OVERRIDE_CATEGORY_FILE.format(year=year)
    if os.path.isfile(override_category_file):
      cat_set.update(open(override_category_file).readlines())
    for c in cat_set:
      key, value = c.split(':')
      values = value.split(',')
      categories[cls.Strip(key)] = cls.Strip(value.split(','))
    # print(categories)
    return categories

  @staticmethod
  def SearchExpression():
    non_tab = r'([^\t]+)'
    opt_non_tab = r'([^\t]*)'
    tab = r'\t'
    return (r'^' + non_tab + tab + opt_non_tab + tab +
            non_tab + tab + non_tab + tab + non_tab + r'$')

  def ProcessMatch(self, m):
    if m.group(1) == 'Date':
      return

    # print(m.string.rstrip())
    description = m.group(2) or m.group(3)
    value = float(m.group(4).replace(',',''))

    found = False
    for category in self.parsed_results.keys():
      if description.find(category) == 0:
        d = self.parsed_results[category]
        d['count'] += 1
        d['total'] += value
        found = True
        break
    if not found:
      raise Exception('Unknown description: %s' % description)

  @staticmethod
  def EmptyResult():
    return {'count': 0, 'total': 0}

  def Search(self):
    self.parsed_results = {key: {'count': 0, 'total': 0} for key in self.categories.keys()}
    utils.SearchFile(self.etrade_file, search_exp=self.SearchExpression(),
                     Process=lambda m: self.ProcessMatch(m))

  def Print(self):
    entries = 0
    results = {}
    # print(self.parsed_results)
    for key in self.parsed_results.keys():
      d = self.parsed_results[key]
      count = d['count']
      total = d['total']
      for name in self.categories[key]:
        if not results.has_key(name):
          results[name] = {'count': 0, 'total': 0}
        results[name]['count'] += count
        results[name]['total'] += total
      entries += count
    for key in results.keys():
      print('%s (instances %d): %.2f' %
            (key, results[key]['count'], results[key]['total']))
    return entries

  def Verify(self, entries):
    filelen = len(open(self.etrade_file).readlines())
    if (filelen - entries) != 1:
      raise Exception('Unexpected entries: filelen=%d, entries=%d'
                      % (filelen, entries))

  def Run(self):
    self.Search()
    entries = self.Print()
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
