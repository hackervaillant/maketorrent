#!/usr/bin/env python3
#
#  bdecode.py
#

import bencode

D, E, I, L = 100, 101, 105, 108
COLON = 58
DIGITS = range(48, 58)


def Bdecode(data):

    return dispatch(bytearray(data))
    

def dispatch(data):
    
    if data[0] == L:
        return bdecode_list(data)

    elif data[0] == D:
        return bdecode_dict(data)

    elif data[0] == I:
        return bdecode_int(data)
        
    elif data[0] in DIGITS:
        return bdecode_str(data)

    else:
        raise ValueError('Invalid Bencode: unknown data identifier')
    
    
def bdecode_list(data):
    
    ret = []
    data.pop(0)
    
    while data[0] != E:
        ret.append(dispatch(data))
    
    data.pop(0)
            
    if not ret:
        raise ValueError('Invalid Bencode: Empty list')
        
    return ret


def bdecode_dict(data):
    
    ret = {}
    data.pop(0)
    
    while data[0] != E:
        key = dispatch(data)
        value = dispatch(data)
        
        if type(key) != str:
            raise ValueError('Invalid Bencode: Dict keys must be strings')
    
        ret[key] = value
        
    data.pop(0)
    
    if not ret:
        raise ValueError('Invalid Bencode: Empty dict')
        
    return ret


def bdecode_int(data):
    
    ret = bytearray()
    
    while True:
        b = data.pop(0)

        if b == I:
            continue

        elif b in DIGITS:
            ret.append(b)
        
        elif b == E:
            return int(ret)
        
        
def bdecode_str(data):
    
    ints = bytearray()
    ret = bytearray()

    while True:
        b = data.pop(0)
        
        if b in DIGITS:
            ints.append(b)
            
        elif b == COLON:
            length = int(ints)
            break
    
    if not length:
        raise ValueError('Invalid Bencode: Empty string')
    
    for _ in range(length):
        ret.append(data.pop(0))
            
    try:
        return ret.decode()

    except UnicodeDecodeError:
        return bytes(ret)


def main():
    
    native = {'z': ['héhé', 123, 1], 'a': 'foo', 'x': b'\x01\xff'}
    bencoded = b'd1:a3:foo1:x2:\x01\xff1:zl6:h\xc3\xa9h\xc3\xa9i123ei1eee'
    
    try:
        assert bencode.Bencode(native) == bencoded, 'encode'
        assert Bdecode(bencoded) == native, 'decode'

    except AssertionError as e:
        return e
        
    else:
        return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
