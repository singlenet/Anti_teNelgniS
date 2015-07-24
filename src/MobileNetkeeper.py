#!/usr/bin/env python
# coding=utf-8

import re
from hashlib import md5
from requests import session

import pyAes as AES


class MobileNetkeeper(object):
    INIT_KEY = '7%ChIna3#@Net*%'
    _UUID = '261D80CF8890F63571350565F605174746C2B3E294CA37A6E993A155BF3CFE51'
    _HEADERS = {
        'User-Agent': 'China Telecom Client',
        'Accept': '*/*',
        'Accept-Language': 'zh-Hans, en, fr, de, ja, nl, it, es, pt, pt-PT, da, fi, nb, sv, ko, zh-Hant, ru, pl, tr, uk, ar, hr, cs, el, he, ro, sk, th, id, ms, en-GB, ca, hu, vi, en-us;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Accept-Encoding': 'gzip, deflate',
    }

    def __init__(self, username, UUID=None):
        self.username = username
        if UUID is not None:
            self._UUID = UUID

        self.session = session()
        self.session.headers = self._HEADERS

    @classmethod
    def encrypt_password(cls, password):
        aes_key = md5(cls.INIT_KEY).digest()
        aes = AES.new(aes_key, AES.MODE_ECB)

        # padding
        l = 16 - len(password) % 16
        ram_data = password + l * chr(l)
        ram_data = ram_data.encode('utf-8')

        return aes.encrypt(ram_data).encode('hex').upper()

    def update_uuid(self, new_uuid):
        self._UUID = new_uuid

    def request_uuid(self, ipaddress=None):
        params = {
            'wlanuserip': ipaddress,
            'acname': 'BPSS_BRAS_1'
        }

        req = self.session.post(url='http://115.239.134.163:8080/showlogin.do',
                                data=params,
                                timeout=5)
        searched = re.search(r'<Uuid>([A-Z0-9]{64})</Uuid>', req.content)
        if searched:
            return searched.group(1)
        raise Exception('Request UUID failed.')

    def http_login(self, password, ipaddress):
        self._UUID = self.request_uuid(ipaddress)

        login_params = {
            'ratingtype': '1',
            'password': self.encrypt_password(password),
            'uuid': self._UUID,
            'userip': ipaddress,
            'username': self.username,
            'acname': 'BPSS_BRAS_1',
        }

        req = self.session.post(url='http://115.239.134.163:8080/servlets/G3loginServlet',
                                data=login_params,
                                timeout=5)
        searched = re.search(r'<ResponseCode>(\d.*)</ResponseCode>', req.content)
        if searched is not None:
            return int(searched.group(1)), self._UUID
        raise Exception('Request login failed.')

    def http_logout(self, ipaddress):
        logout_params = {
            'userip': ipaddress,
            'ratingtype': '1',
            'uuid': self._UUID
        }

        req = self.session.post(url='http://115.239.134.163:8080/servlets/G3logoutServlet',
                                data=logout_params,
                                timeout=5)
        searched = re.search(r'<ResponseCode>(\d.*)</ResponseCode>', req.content)
        if searched is not None:
            return int(searched.group(1))
        raise Exception('Request logout failed')


if __name__ == '__main__':
    pass