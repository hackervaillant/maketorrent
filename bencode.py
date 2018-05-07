#!/usr/bin/env python3
#
#  bencode.py
#

import bdecode


def Bencode(var):
    vartype = type(var)
    varfunc = {int: bencode_integer,
               bool: bencode_boolean,
               str: bencode_string,
               bytes: bencode_bytes,
               list: bencode_list,
               tuple: bencode_list,
               dict: bencode_dict}

    return varfunc[vartype](var)
    
    
def bencode_bytes(var):
    return str(len(var)).encode() + b':' + var


def bencode_string(var):
    return bencode_bytes(var.encode())


def bencode_integer(var):
    return b'i' + str(var).encode() + b'e'


def bencode_boolean(var):
    return b'i1e' if var else b'i0e'


def bencode_list(var):
    ret = b'l'

    for item in var:
        ret += Bencode(item)

    return ret + b'e'


def bencode_dict(var):
    ret = b'd'

    for key, value in sorted(var.items(), key=lambda x: x[0]):
        ret += Bencode(key) + Bencode(value)

    return ret + b'e'


def main():

    native = {'z': ['héhé', 123, 1], 'a': 'foo', 'x': b'\x01\xff'}
    bencoded = b'd1:a3:foo1:x2:\x01\xff1:zl6:h\xc3\xa9h\xc3\xa9i123ei1eee'
    
    try:
        assert Bencode(native) == bencoded, 'encode'
        assert bdecode.Bdecode(bencoded) == native, 'decode'

    except AssertionError as e:
        return e
        
    else:
        return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
