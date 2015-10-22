#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
from imma_parser import parse_line, log
from hbase_mappings import get_data
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
    writes a key starting with a timestamp is good for me.
    Geo position should also be included for uniqueness.
    TODO: how to optimize searches by geo position?

    So, the key is: <timestamp><latitude><longitude><random>
        timestamp - string in the form YYmmddHHMM:
                     197101171600 for tea time on 1st of January 1971
        latitude, longitude - as decimal degrees without the decimal point
                    and left filled with zeros
                    to make 5 symbols: 04269 02332 for Sofia
        random - 4 random symbols to distinguish between keys with
                    equal first part
        so, for 1971-01-01 16:00 in Sofia wi may have:
                    1971011716000426902332xxxx
    '''
    key_format = '{year:0>4d}{month:0>2d}{day:0>2d}{hour:0>4d}' + \
                 '{latitude}{longitude}{rand}'
    data_dict = dict(data)
    latitude = '{:0>6.2f}'.format(data_dict['LAT']).replace('.', '')
    longitude = '{:0>6.2f}'.format(data_dict['LON']).replace('.', '')
    key = key_format.format(year=data_dict['YR'],
                            month=data_dict['MO'],
                            day=data_dict['DY'],
                            hour=data_dict['HR'],
                            latitude=latitude,
                            longitude=longitude,
                            rand=id_generator())
    return key


def hbase_write(connection, table_name, family, key, data):
    table = connection.table(table_name)
    table.put(key, get_data(data, family))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This tool parses text file in the '
                    'International Maritime Meteorological '
                    'Archive (IMMA) Form '
                    'and save the results in hbase database')
    parser.add_argument('-in', '--infile',
                        help='File to read from (stdin if not specified)')
    parser.add_argument('-t', '--datatable', default='meteo:icoads',
                        help='Data table to write to'
                             '(defaults to "meteo:icoad")')
    parser.add_argument('-f', '--column-family', default='d',
                        help='Column family to write to (defaults to "d")')
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
    connection = happybase.Connection(host=args.host, port=args.port)

    line_number = 0
    for line in input_file:
        try:
            line_number += 1
            if args.from_line and args.from_line > line_number:
                continue
            if args.to_line and args.to_line < line_number:
                break
            data = parse_line(line)
            key = get_key(data)
            if args.unparsed:
                log('WARNING', '--unparsed not supported yet')
                exit(-1)
            else:
                if args.debug:
                    log('INFO', 'Writing {line} to HBase'.
                        format(line=', '.join([str(d[1]) for d in data])))
                hbase_write(connection, args.datatable, args.column_family,
                            key, data)
        except Exception, e:
            log('ERROR',
                'Error parsing line "{}".\n'
                'The error message was "{}"'.format(line, e.message))
