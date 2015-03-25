#!/usr/bin/env python
# coding=utf-8


def security_encode(pwd, key='RDpbLfCPsJZ7fiv'):
    charbox = ('yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciX'
               'TysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgML'
               'wygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3'
               'sfQ1xtXcPcf1aT303wAQhv66qzW')

    keyl = len(key)
    pwdl = len(pwd)
    charboxl = len(charbox)

    times = keyl if keyl > pwdl else pwdl

    ciphertext = ''
    for index in xrange(times):
        cl = cr = 0xBB

        if index >= keyl:
            cr = ord(pwd[index])
        elif index >= pwdl:
            cl = ord(key[index])
        else:
            cl = ord(key[index])
            cr = ord(pwd[index])

        ciphertext += charbox[(cl ^ cr) % charboxl]

    return ciphertext

if __name__ == '__main__':
    print security_encode('537953795379')
