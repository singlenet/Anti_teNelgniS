import time
import struct
from SNConstants import HNSNAccount


def hash_key(key_str):
    length = len(key_str)
    result = 0
    fmt_str = '<%dH' % (length / 2)

    if length % 2:
        result = ord(key_str[-1])
        key_str = key_str[:-1]

    result += sum(struct.unpack(fmt_str, key_str))

    if result & 0xFFFF0000:
        result = ((result >> 0x10) + result) & 0xFFFF

    result = ~result & 0xFFFF
    return result


def new_calc_pin(username, share_key=HNSNAccount['SHARE_KEY'], sec_key=HNSNAccount['SEC_KEY'], timestamp=None):
    KEY_TABLE = HNSNAccount['KEY_TABLE']

    timestamp = (timestamp or int(time.time())) & 0xFFFFFFFF

    first_key = struct.pack(
        '>I', timestamp) + share_key + username.split('@')[0]
    first_hash = hash_key(first_key)

    second_key = struct.pack('>H', first_hash) + sec_key
    second_hash = hash_key(second_key)

    final_key = struct.pack('>H', timestamp >> 16)
    final_key += struct.pack('<H', first_hash)
    final_key += struct.pack('>H', timestamp & 0xFFFF)
    final_key += struct.pack('<H', second_hash)

    final_table = map(ord, final_key)

    vectors = []
    for i in xrange(1, 8, 2):
        vectors.append(final_table[i - 1] >> 0x3 & 0x1F)
        vectors.append(
            ((final_table[i - 1] & 0x7) << 0x2) | (final_table[i] >> 0x6 & 0x3))
        vectors.append(final_table[i] & 0x3F)

    result = map(lambda position: KEY_TABLE[position % 64], vectors)
    return '~LL_%s_' % ''.join(result)

if __name__ == '__main__':
    pass
