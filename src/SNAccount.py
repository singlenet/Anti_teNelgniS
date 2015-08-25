#!/usr/bin/env python
# coding=utf-8
import re
import time
import struct
import hashlib
from SNConstants import NKAccount

# copy from https://github.com/nowind/sx_pi/

def check_username(username):
    return True if re.search(r'\d{6,15}@[a-z]{2,4}\.xy', username, re.IGNORECASE) else False

def calc_pin(username, share_key=NKAccount['SHARE_KEY'], prefix='\x0D\x0A'):
    assert check_username(username=username)
    username = username.upper()

    time_div_by_five = int(time.time()) / 5
    time_div_by_five = 288023653

    time_hash = [0] * 4
    for i in xrange(4):
        for j in xrange(8):
            time_hash[i] = time_hash[i] + (((time_div_by_five >> (i + 4 * j)) & 1) << (7 - j))

    pin27_byte = [0] * 8
    pin27_byte[0] = ((time_hash[0] >> 2) & 0x3F)
    pin27_byte[1] = ((time_hash[0] & 0x03) << 4 & 0xff) | ((time_hash[1] >> 4) & 0x0F)
    pin27_byte[2] = ((time_hash[1] & 0x0F) << 2 & 0xff) | ((time_hash[2] >> 6) & 0x03)
    pin27_byte[3] = time_hash[2] & 0x3F
    pin27_byte[4] = ((time_hash[3] >> 2) & 0x3F)
    pin27_byte[5] = ((time_hash[3] & 0x03) << 4 & 0xff)
    for i in xrange(6):
        pin27_byte[i] = {True: (pin27_byte[i] + 0x20) & 0xff,
                         False: (pin27_byte[i] + 0x21) & 0xff}[((pin27_byte[i] + 0x20) & 0xff) < 0x40]

    pin27_str = ''
    for i in xrange(6):
        pin27_str = pin27_str + chr(pin27_byte[i])

    before_md5 = struct.pack('>I', time_div_by_five) + username.split('@')[0] + share_key
    pin89_str = hashlib.md5(before_md5).hexdigest()[0:2]

    pin = prefix + pin27_str + pin89_str
    return pin

if __name__ == '__main__':
    pass