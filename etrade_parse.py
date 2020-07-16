#!/usr/bin/python

import argparse
import os
import sys

import utils


class EtradeParser(object):

  ETRADE_DIR = os.path.join(utils.HOME_DIR, 'Documents', 'etrade')
  ETRADE_FILE = os.path.join(ETRADE_DIR, 'etrade_{year}.txt')
  DEFAULT_YEAR = 2019
  CATEGORY_FILE = os.path.join(ETRADE_DIR, 'etrade_categories.txt')
  CATEGORY_FILE = os.path.join(
      os.path.join(os.path.dirname(__file__), 'etrade_categories.txt'))


  def __init__(self, category_file, etrade_file):
    self.category_result = {}
    self.etrade_file = etrade_file
    self.categories = self.InitCategories(category_file)

  @classmethod
  def InitCategories(cls, category_file):
    categories = {}
    ary = open(category_file).readlines()
    for c in ary:
      key, value = c.split(':')
      categories[key.strip("' ")] = value.strip("' \n")
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
    for category in self.category_result.keys():
      if description.find(category) == 0:
        ary = self.category_result[category]
        ary[0] += 1
        ary[1] += value
        found = True
        break
    if not found:
      raise Exception('Unknown description: %s' % description)

  def Run(self):
    self.category_result = {key: [0, 0] for key in self.categories.keys()}
    utils.SearchFile(self.etrade_file, search_exp=self.SearchExpression(),
                     Process=lambda m: self.ProcessMatch(m))
    entries = self.PrintEntries()
    self.VerifyEntries(entries)

  def PrintEntries(self):
    entries = 0
    for key in self.category_result.keys():
      name = self.categories[key]
      result = self.category_result[key]
      entries += result[0]
      print('%s (instances %d): %.2f' % (name, result[0], result[1]))
    return entries

  def VerifyEntries(self, entries):
    filelen = len(open(self.etrade_file).readlines())
    if (filelen - entries) != 1:
      raise Exception('Unexpected entries: filelen=%d, entries=%d'
                      % (filelen, entries))

  @classmethod
  def ParseArgs(cls, argv):
    parser = argparse.ArgumentParser('Parse Etrade bank statements')
    parser.add_argument('--year', default=cls.DEFAULT_YEAR,
                        help='default %s' % cls.DEFAULT_YEAR)
    parser.add_argument('--file', default=cls.ETRADE_FILE,
                        help='default %s' % cls.ETRADE_FILE)
    parser.add_argument('--category-file', default=cls.CATEGORY_FILE,
                        help='default %s' % cls.CATEGORY_FILE)
    return parser.parse_known_args(argv[1:])


def main(argv):
  opts, rem = EtradeParser.ParseArgs(argv)

  if rem:
    raise Exception('Unknown args: %s' % rem)

  EtradeParser(opts.category_file, opts.file.format(year=opts.year)).Run()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
