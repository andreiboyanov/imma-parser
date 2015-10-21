#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
from imma_formats import TABLES


def log(level, message):
    sys.stderr.write('[{level}] {message}'.format(level=level,
                                                  message=message))


def get_key(data):
    key_format = '{year:0>4d}{month:0>2d}{day:0>2d}{hour:0>4d}' + \
            '{latitude}{longitude}'
    data_dict = dict(data)
    latitude = '{:0>6.2f}'.format(data_dict['LAT']).replace('.', '')
    longitude = '{:0>6.2f}'.format(data_dict['LON']).replace('.', '')
    key = key_format.format(year=data_dict['YR'],
                            month=data_dict['MO'],
                            day=data_dict['DY'],
                            hour=data_dict['HR'],
                            latitude=latitude,
                            longitude=longitude)
    return key


def parse_line(line):
    '''
    Parses a line in the IMMA format
    (http://icoads.noaa.gov/e-doc/imma/R2.5-imma_short.pdf)
    '''
    data, index = parse_attachment(line, 'c0', 0)
    return data


def parse_attachment(line, table_name, start_index=0):

    def convert_value(data_type, string_value):
        if ' ' * len(string_value) == string_value:
            return data_type(0)
        else:
            return data_type(string_value)

    def log_conversion(variable_name, data_type, value):
        log('ERROR', 'Value error for variable {name}: '
                     '{data_type}({value}).\n'
                     'Exception was "{error_message}"'.
            format(name=variable_name, data_type=data_type.__name__,
                   value=value, error_message=e.message))

    data = list()
    for column in TABLES[table_name]:
        no, data_type, size, name, description, min_value, max_value, units =\
            column
        string_value = line[start_index:start_index + size]
        try:
            value = convert_value(data_type, string_value)
        except ValueError, e:
            log_conversion(name, data_type, string_value)
        data.append((name, value))
        start_index += size
    return data, start_index

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This tool parses text file in the '
                    'International Maritime Meteorological '
                    'Archive (IMMA) Form '
                    'and out them in csv format')
    parser.add_argument('-in', '--infile',
                        help='File to read from (stdin if not specified)')
    parser.add_argument('-out', '--outfile',
                        help='File to write to (stdout if not specified)')
    parser.add_argument('-u', '--unparsed', action='store_true',
                        help='Writes only the key and the unparsed line')
    parser.add_argument('-from', '--from-line', type=int,
                        help='Output starting from <from_line>')
    parser.add_argument('-to', '--to-line', type=int,
                        help='Output ending at <to_line>')

    args = parser.parse_args()
    input_file = args.infile and open(args.infile) or sys.stdin
    output_file = args.outfile and open(args.outfile, 'a+') or sys.stdout

    line_number = 0 
    for line in input_file:
        line_number += 1
        if args.from_line and args.from_line > line_number:
            continue
        if args.to_line and args.to_line < line_number:
            break
        data = parse_line(line)
        key = get_key(data)
        if args.unparsed:
            output_file.write(', \n'.join((key, line)))
        else:
            output_file.write(','.join([key, ] +
                              [str(element[1]) for element in data]) + '\n')
