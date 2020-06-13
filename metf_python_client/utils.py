# -*- coding: utf-8 -*-
from struct import unpack, calcsize


class DataStruct:
    """
    fields = [  # name, struct format
            ('version',   'B'), # unsigned char
            ('service',   'H'), # unsigned short
            ('impulses1', 'L'), # unsigned long
    ]
    """
    def __init__(self, fields, buffer=None):

        if buffer:

            fmt = ''.join([f[1] for f in fields])

            t = unpack('<' + fmt, buffer)

            for i in range(len(fields)):
                self.__dict__[fields[i][0]] = t[i]

    @staticmethod
    def calcsize(fields, target=None):
        """
        :param fields: list of tuples [(name, format), (), ... ]
        :param target: stop at this field
        :return: structure native size in bytes
        """
        fmt = ''
        for f in fields:
            if target is not None and f[0] == target:
                break
            else:
                fmt += f[1]

        return calcsize('='+fmt)  # Native alignment


def str2hex(s):
    """
    :param s: '303132'
    :return: '123'
    """
    return ''.join([chr(c) for c in bytearray.fromhex(s)])


def hex2str(data):
    """
    :param data: '123'
    :return: '303132'
    """
    return ''.join('{:02X}'.format(ord(c)) for c in data)


def str2array(s):
    """
    :param s: '303132'
    :return: [30, 31, 32]
    """
    return bytearray.fromhex(s)
