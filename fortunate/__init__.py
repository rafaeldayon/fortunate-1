#!/usr/bin/env python
from __future__ import print_function, with_statement

import os
import sys
import random
import hashlib
from optparse import OptionParser

if sys.version_info[0] < 3:
    import cPickle as pickle
    import string
else:
    import pickle
    string = str


__all__ = ['Fortunate']

__version__ = "1.0.0"
__author__ = "German Mendez Bravo (Kronuz), Brian M. Clapper"
__email__ = "german.mb@gmail.com, bmc@clapper.org"
__url__ = "https://github.com/Kronuz/fortunate"
__copyright__ = "2018 German Mendez Bravo (Kronuz), 2008-2011 Brian M. Clapper"
__license__ = "BSD-style license"


FORTUNE_FILE = os.path.join(os.path.dirname(__file__), 'fortunes')


class Fortunate(object):
    rot13 = string.maketrans("ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

    def __init__(self, fortune_files, fortune_index_file=None, verbose=False, force_update=False):
        if isinstance(fortune_files, (list, tuple)):
            self.fortune_files = set(fortune_files)
        else:
            self.fortune_files = set([fortune_files])
        if not self.fortune_files:
            raise AttributeError("Must specify at least one fortune file")
        if fortune_index_file is None:
            md5 = hashlib.md5()
            for file in sorted(self.fortune_files):
                md5.update(file.encode('utf-8'))
            fortune_index_file = os.path.expanduser(os.path.join('~', '.fortunate', md5.hexdigest() + '.dat'))
            try:
                os.makedirs(os.path.expanduser(os.path.join('~', '.fortunate')))
            except OSError:
                pass
        self.fortune_index_file = fortune_index_file
        self.verbose = verbose
        self.force_update = force_update

    def fortune_file(self, filename):
        if not hasattr(self, '_fortunes'):
            self._fortunes = {}
        try:
            fortune_file = self._fortunes[filename]
        except KeyError:
            fortune_file = self._fortunes[filename] = open(filename, 'r')
        return fortune_file

    @property
    def fortune_index(self):
        if not hasattr(self, '_index'):
            if self.force_update or not os.path.exists(self.fortune_index_file):
                self.update()
            else:
                with open(self.fortune_index_file, 'rb') as fortune_index_file:
                    self._index = pickle.load(fortune_index_file)
        return self._index

    def read_fortunes(self, filename):
        result = []
        start = None
        pos = 0
        for line in filename:
            if line == "%\n":
                if pos == 0:  # "%" at top of file. Skip it.
                    continue
                yield (start, pos - start, ''.join(result))
                result = []
                start = None
            else:
                if start is None:
                    start = pos
                result.append(line)
            pos += len(line)

        if result:
            yield (start, pos - start, ''.join(result))

    def update(self):
        self._index = []

        if self.verbose:
            print("Updating '%s' from: %s" % (self.fortune_index_file, ', '.join(self.fortune_files)))

        filenames = set()
        for file in self.fortune_files:
            if os.path.isdir(file):
                for root, folders, files in os.walk(file):
                    for filename in files:
                        if not filename.endswith('.dat'):
                            filename = os.path.join(root, filename)
                            filenames.add(filename)
            elif os.path.exists(file):
                filenames.add(file)
            elif self.verbose:
                print("Skipping non-existent '%s'" % file)

        shortest = None
        longest = None
        duplicates = 0
        fortunes = set()
        for filename in filenames:
            filename = os.path.abspath(filename)
            for start, length, fortune in self.read_fortunes(self.fortune_file(filename)):
                if fortune in fortunes:
                    duplicates += 1
                else:
                    self._index.append((filename, start, length, '/off/' in filename and '/unrotated/' not in filename))
                    shortest = length if shortest is None else min(shortest, length)
                    longest = length if longest is None else max(longest, length)
                    fortunes.add(fortune)

        with open(self.fortune_index_file, 'wb') as index_file:
            pickle.dump(self._index, index_file, 0)

        if self.verbose:
            print("Updated %d fortunes.\nLongest: %d\nShortest: %d\nDuplicates: %d" %
                (len(self._index), longest, shortest, duplicates))

    def __call__(self):
        filename, start, length, rotated = self.fortune_index[random.randint(0, len(self.fortune_index) - 1)]
        fortune_file = self.fortune_file(filename)
        fortune_file.seek(start)
        fortune = fortune_file.read(length)
        if rotated:
            fortune = string.translate(fortune, self.rot13)
        return fortune


def main():
    """
    Main program.
    """
    usage = "Usage: %s [OPTIONS] [fortune_files ...]" % os.path.basename(sys.argv[0])
    epilog = "If <fortune_files> are omitted, fortune looks at the " \
             "FORTUNE_FILE environment variable for the path."
    arg_parser = OptionParser(usage=usage, epilog=epilog)
    arg_parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                          help="when updating the index file, emit verbose messages")
    arg_parser.add_option('-u', '--update', action='store_true', dest='update',
                          help="update the index file, instead of printing a fortune.")
    arg_parser.add_option('-V', '--version', action='store_true',
                          dest='show_version', help="show version and exit.")
    arg_parser.add_option('-n', type='int', default=1,
                          dest='num', help="number of fortune cookies to show")

    options, args = arg_parser.parse_args(sys.argv)
    if len(args) > 1:
        fortune_files = args[1:]
    else:
        try:
            fortune_files = os.environ['FORTUNE_FILE'].split(':')
        except KeyError:
            if os.path.isdir('/usr/local/share/games/fortunes'):
                fortune_files = ['/usr/local/share/games/fortunes']
            elif os.path.isdir('/usr/share/games/fortunes'):
                fortune_files = ['/usr/share/games/fortunes']
            elif os.path.exists(FORTUNE_FILE):
                fortune_files = []
            else:
                arg_parser.error("Missing fortune file.")
            fortune_files.append(FORTUNE_FILE)

    try:
        if options.show_version:
            print("fortune, version %s" % __version__)
        else:
            generator = Fortunate(fortune_files, verbose=options.verbose, force_update=options.update)
            for i, _ in enumerate(range(options.num)):
                if i:
                    sys.stdout.write("%\n")
                sys.stdout.write(generator())
    except ValueError as msg:
        print(msg, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
