# coding=utf8

'''
Copyright 2015 heming.keh@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from __future__ import print_function
from __future__ import unicode_literals
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)


# The class MUST call this class decorator at creation time
@magics_class
class FindMagics(Magics):

    @line_magic("find")
    def findFilesByRe(self, line):
        # Note: we need import modules here,
        # because ipython 'reset' command not reload all 'my_magic.py'
        import shlex
        import argparse
        import os
        import sys
        import re

        def parse_type(s):
            '''parse argument '-t'
            '''
            if s not in ['a', 'f', 'd']:
                raise argparse.ArgumentTypeError(
                    'type must be "a" or "f" or "d"')
            return s

        def parse_path(s):
            '''parse argument 'path'
            '''
            if not os.path.isdir(s):
                raise argparse.ArgumentTypeError(
                    '"{}" is not directory'.format(s))
            return s

        def parse_re(s):
            '''parse pattern argument
            '''
            try:
                pattern = re.compile(s)
            except re.error as e:
                raise argparse.ArgumentTypeError(
                    '"{}" is not regex, error: {}'.format(s, e))
            return pattern

        UNITS = {'b': 1L, 'k': 1024L, 'm': 1024*1024L, 'g': 1024*1024*1024L}

        def parse_size(s):
            '''parse file size argument
            '''
            if not s:
                return s
            m = re.match('^([<>])(\d+)([bkmg]?)$', s, re.I)
            if m:
                sign, size, unit = m.groups()
                unit = unit.lower()
                if not unit:
                    unit = 'b'
                size = long(size) * UNITS[unit]
                if sign == '>':
                    return lambda x: x >= size
                else:
                    return lambda x: x < size
            else:
                m = re.match('^(\d+)([bkmg]?)~(\d+)([bkmg]?)$', s, re.I)
                if m:
                    min_size, min_size_unit, max_size, max_size_unit = \
                        m.groups()
                    # variance size
                    if not min_size_unit:
                        min_size_unit = 'b'
                    min_size_unit = min_size_unit.lower()
                    min_size = long(min_size) * UNITS[min_size_unit]
                    # size
                    if not max_size_unit:
                        max_size_unit = 'b'
                    max_size_unit = max_size_unit.lower()
                    max_size = long(max_size) * UNITS[max_size_unit]
                    return lambda x: x > min_size and x < max_size
                else:
                    raise argparse.ArgumentTypeError(
                        '"{}" is invalid'.format(s))

        def file_size_fmt(num, unit='b'):
            return '{:,.2f}{}'.format(float(num) / UNITS[unit], unit)

        def parse_format_unit(s):
            if s.lower() not in ['b', 'k', 'm', 'g']:
                raise argparse.ArgumentTypeError('"{}" is invalid'.format(s))
            return s.lower()

        # Note: because shlex not support unicode, so use this trick
        arguments = map(lambda s: s.decode('UTF8'),
                        shlex.split(line.encode('utf8')))
        # parse arguments
        parser = argparse.ArgumentParser(
            description='Search for files in a directory hierarchy',
            prog="find")
        parser.add_argument('-type', '--file-type', default='a',
                            type=parse_type,
                            help='File type, "a" is all types,'
                            ' "f" is regular file, "d" is directory')
        parser.add_argument('-size', '--file-size', type=parse_size,
                            help='File size, ">100M" size greater than 100M,'
                            ' "<100M" size smaller than 100M')
        parser.add_argument('-unit', '--format-unit', default='k',
                            type=parse_format_unit)
        parser.add_argument('path', type=parse_path, help='a folder name')
        parser.add_argument('pattern', type=parse_re,
                            help='a regex pattern to match the file name')
        try:
            args = parser.parse_args(arguments)
        except SystemExit:
            return

        total_size = 0.0
        total_files = 0
        print('{:>14}     {}'.format('SIZE', 'PATH'))
        print('{:>14}     {}'.format('------', '-'*60))
        for root, dirs, files in os.walk(args.path):
            for name in (files + dirs):
                absolute_name = os.path.join(root, name)
                if args.file_type == 'f' and not os.path.isfile(absolute_name):
                    continue
                if args.file_type == 'd' and not os.path.isdir(absolute_name):
                    continue
                if not re.search(args.pattern, name):
                    continue
                if os.name == 'nt':
                    absolute_name = absolute_name.replace('/', os.path.sep)
                absolute_name = os.path.abspath(absolute_name)
                if len(absolute_name) > 260:  # MAX_PATH
                    continue
                if args.file_size:
                    file_size = os.path.getsize(absolute_name)
                    # is file size match
                    if args.file_size(file_size):
                        print('{:>14}     {}'.format(
                            file_size_fmt(file_size, args.format_unit),
                            absolute_name))
                        total_files += 1
                        total_size += file_size
                else:
                    print('{:>14}     {}'.format('-', absolute_name))
                    total_files += 1
        print('{:>14}     {}'.format('------', '-'*60))
        if args.file_size:
            print('{:>14}     {} files'.format(
                file_size_fmt(total_size, args.format_unit),
                total_files))
        else:
            print('{:>14}     {} files'.format('-', total_files))


# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(FindMagics)
