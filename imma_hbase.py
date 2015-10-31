#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
from imma_parser import parse_line, log
import happybase
import string
import random

ID_CHARS = string.ascii_uppercase + string.digits


def id_generator(size=4, chars=ID_CHARS):
    result = ''.join(random.choice(chars) for i in xrange(size))
    return result


def get_key(data):
    '''
    Returns a value to use as HBase row key. As I don't care about slow
    writes a timestamp key is good for me.
    Geo positions are used as columns.

    So, the key is: YYYYmmddHHMM
    '''
    key_format = '{year:0>4d}{month:0>2d}{day:0>2d}{hour:0>4d}'
    key = key_format.format(year=data['YR'],
                            month=data['MO'],
                            day=data['DY'],
                            hour=data['HR'])
    return key


def get_column(data):
    '''
    Return the column name to write to (without the family qualifier).
    I'll use the rounded to integers Longitude and Latitude for column names.
    I hope that this will give me very performant search for meteo data
    '''
    latitude = int(round(data['LAT']))
    longitude = int(round(data['LON']))
    return '{:0=-3d}{:0=-3d}'.format(latitude, longitude)


def get_value(data):
    '''
        Value to write to the database cell.
        It's just the string represantation of the imma data as dictionary
    '''
    return repr(data)


def hbase_write(connection, table_name, family, data):
    table = connection.table(table_name)
    key = get_key(data)
    value = get_value(data)
    column = family + ':' + get_column(data)
    table.put(key, {column: value}, wal=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This tool parses text file in the '
                    'International Maritime Meteorological '
                    'Archive (IMMA) Form '
                    'and save the results in hbase database')
    parser.add_argument('-in', '--infile',
                        help='File to read from (stdin if not specified)')
    parser.add_argument('-out', '--outfile',
                        help='File to write row keys to '
                             '(stdout if not specified)')
    parser.add_argument('-t', '--datatable', default='meteo:icoads',
                        help='Data table to write to'
                             '(defaults to "meteo:icoad")')
    parser.add_argument('-f', '--column-family', default='c',
                        help='Column family to write to (defaults to "c")')
    parser.add_argument('-host', '--host', help='HBase host',
                        default='localhost')
    parser.add_argument('-p', '--port', help='HBase port', type=int,
                        default=9090)
    parser.add_argument('-u', '--unparsed', action='store_true',
                        help='Writes only the key and the unparsed line')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Write debug messages')
    parser.add_argument('-from', '--from-line', type=int,
                        help='Output starting from <from_line>')
    parser.add_argument('-to', '--to-line', type=int,
                        help='Output ending at <to_line>')

    args = parser.parse_args()
    input_file = args.infile and open(args.infile) or sys.stdin
    output_file = args.outfile and open(args.outfile) or sys.stdout
    connection = happybase.Connection(host=args.host, port=args.port)

    line_number = 0
    for line in input_file:
        try:
            line_number += 1
            if args.from_line and args.from_line > line_number:
                continue
            if args.to_line and args.to_line < line_number:
                break
            data = dict(parse_line(line))
            if args.unparsed:
                log('WARNING', '--unparsed not supported yet')
                exit(-1)
            else:
                if args.debug:
                    value = get_value(data)
                    column = args.column_family + ':' + get_column(data)
                    log('INFO', 'Writing {key}:{column} ==> {data} to HBase'.
                        format(key=get_key(data), column=column, data=value))
                else:
                    output_file.write(get_key(data) + '\n')
                hbase_write(connection, args.datatable, args.column_family,
                            data)
        except Exception, e:
            log('ERROR',
                'Error parsing line "{}".\n'
                'The error message was "{}"'.format(line, e.message))
