#!/usr/bin/env python3

d = 100
e = 101
i = 105
l = 108
DIGITS = range(48, 58)
colon = 58

class BencodeError(ValueError):
    pass
    

def bdecode(data):
    print(data)
    
    if data[0] == l:
        return bdecode_list(data)

    elif data[0] == d:
        return bdecode_dict(data)

    elif data[0] == i:
        return bdecode_int(data)
        
    elif data[0] in DIGITS:
        return bdecode_str(data)

    else:
        raise BencodeError('Invalid Bencode')
    
    
def bdecode_list(data):
    
    ret = []
    data.pop(0)
    
    while data[0] != e:
        ret.append(bdecode(data))
    
    data.pop(0)        
    return ret


def bdecode_dict(data):
    
    ret = {}
    data.pop(0)
    
    while data[0] != e:
        key = bdecode(data)
        value = bdecode(data)
        
        if type(key) == str:
            ret[key] = value
            
        else:
            raise BencodeError('Dict keys must be strings')

    data.pop(0)
    return ret


def bdecode_int(data):
    
    ret = bytearray()
    
    while True:
        b = data.pop(0)

        if b == i:
            continue

        elif b in DIGITS:
            ret.append(b)
        
        elif b == e:
            return int(ret)
        
        
def bdecode_str(data):
    
    ints = bytearray()
    ret = bytearray()

    while True:
        b = data.pop(0)
        
        if b in DIGITS:
            ints.append(b)
            
        elif b == colon:
            length = int(ints)
            break
    
    for _ in range(length):
        ret.append(data.pop(0))
            
    try:
        return ret.decode()

    except UnicodeDecodeError:
        return bytes(ret)

        


def main():
    
    # bdecode.py

    TEST = b'd1:a3:foo1:x2:\x01\xff1:zl6:h\xc3\xa9h\xc3\xa9i123ei1eee'
    TESTRESULT = {'z': ['héhé', 123, True], 'a': 'foo', 'x': b'\x01\xff'}

    #~ print(bdecode(bytearray(b'i456e')))
    #~ print(bdecode(bytearray(b'4:haha')))
    #~ print(bdecode(bytearray(b'l4:hahae')))
    print(bdecode(bytearray(b'l4:hah5i785ee')))
    print(bdecode(bytearray(TEST)))
    #~ print(bdecode(bytearray(b'ldi32e4:hahaee')))
    #~ print(bdecode(bytearray(b'li32eeli32ee')))

    return 0



if __name__ == '__main__':
    import sys
    sys.exit(main())
