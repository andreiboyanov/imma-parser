# -*- coding: utf-8 -*-

from imma_formats import TABLE_C0
# import struct


def pack(value):
    return str(value)
#    if type(value) == int:
#        return struct.pack('d', value)
#    elif type(value) == float:
#        return struct.pack('f', value)
#    elif type(value) == str:
#        return value
#    else:
#        raise ValueError(value)


def get_data(data, family):
    result = dict()
    data = dict(data)
    for no, t, length, name, description, minimum, maximum, units in \
            TABLE_C0:
        result[family + ':' + name] = pack(data[name])
    return result
