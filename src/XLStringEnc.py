#!/usr/bin/env python
# coding=utf-8


class XLStringEnc(object):

    """
    usage:
        xl = XLStringEnc()
        print xl.decrypt('e4b5faf2c04576af98fa3dd354d32da2')
        print xl.encrypt('xlzjhrprotocol3x')
    """

    base_key = 'f12acd03b45e9678'
    base_box = ('SDJJLKNASDHFUIAk'
                'hfu340985LIASDJF'
                'OISDLKJFOIESJFDK'
                'SMFMLKdLKASDJFOI'
                'DJKKfhisdfisdfks'
                'OIAJEFJLKALSDKFj'
                'kdhfiehsdKA')

    def update_basestring(self, base_key, base_box):
        self.base_key = base_key
        self.base_box = base_box

    def decrypt(self, ciphertext):
        length = len(ciphertext)
        assert length > 2

        plaintext = ''
        for k in xrange(length / 2):
            m = k * 2
            step = ciphertext[m:m + 2]

            # for i in xrange(16):
            #     if self.base_key[i] == step[0]:
            #         break
            # for j in xrange(16):
            #     if self.base_key[j] == step[1]:
            #         break
            i = self.base_key.find(step[0])
            j = self.base_key.find(step[1])

            # print step, i, j, m
            plaintext += chr(
                ord(self.base_box[(m / 2) % 40]) ^ (i | (16 * (i ^ j))))

        return plaintext

    def encrypt(self, plaintext):
        length = len(plaintext)
        assert length > 0

        ciphertext = ''
        for k, c in enumerate(plaintext):
            temp_num = ord(c) ^ ord(self.base_box[k % 40])
            i, j = self._brute_force(temp_num)
            ciphertext += self.base_key[i] + self.base_key[j]

        return ciphertext

    def _brute_force(self, value):
        for i in xrange(16):
            for j in xrange(16):
                if (i | (16 * (i ^ j))) == value:
                    return i, j


class SNStringEnc(XLStringEnc):

    """
    usage:
        sn = SNStringEnc()
        print sn.decrypt('b413f30110a9')
    """

    base_key = 'f18a9d03c45e267'
    base_box = ('WYHNIKmkEDCYHNig'
                'LcdAUJMFBVNEDCGW'
                'SXLYUIEWERTIXCVB'
                '2NM0E1SDF4QAS4YH'
                'N1FGU4SRwKMBaERT'
                'nSDRgPOIlMNB2RTY'
                '0GHU1KIH4FD414')


if __name__ == '__main__':
    xl = XLStringEnc()
    print xl.decrypt('e4b5faf2c04576af98fa3dd354d32da2')
