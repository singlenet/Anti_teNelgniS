#!/usr/bin/env python
# coding=utf-8

import time
import struct
import hashlib
import SNAttribute
from SNConstants import HBDefault, SNClient


class SNHeartBeat(object):

    def __init__(self, code, timestamp, attribute_list, magic_num=0x534E):
        self.code = code
        self.timeflag = self.calc_timeflag(timestamp=timestamp)
        self.magic_num = magic_num
        self.attribute_list = attribute_list

        self._fmt_str = '>HHBB16s'

    @property
    def attributes_data(self):
        attributes_data = ''
        for attribute in self.attribute_list:
            attributes_data += attribute.digest()
        return attributes_data

    @property
    def length(self):
        return struct.calcsize(self._fmt_str) + len(self.attributes_data)

    @property
    def signature(self):
        salt = HBDefault['SIG_SALT']

        temp_data = struct.pack(self._fmt_str, self.magic_num,
                                self.length, self.code,
                                self.timeflag, '\x00' * 16)
        temp_data += self.attributes_data

        m = hashlib.md5()
        m.update(temp_data)
        m.update(salt)

        return m.digest()

    @classmethod
    def calc_timeflag(cls, timestamp=int(time.time())):
        temp_num = (((timestamp * 0x343FD) + 0x269EC3) & 0xFFFFFFFF)
        timeflag = (temp_num >> 0x10) & 0xFF
        return timeflag

    def digest(self):
        ramdata = struct.pack(self._fmt_str, self.magic_num,
                              self.length, self.code,
                              self.timeflag, self.signature)
        ramdata += self.attributes_data
        return ramdata

    def hexdigest(self):
        return self.digest().encode('hex')


class SNThunderProtocol(SNHeartBeat):

    def __init__(self, username, ipaddress, timestamp, version=SNClient['CLIENT_VERSION']):
        #timestamp = 1424526603
        attribute_list = [
            SNAttribute.CLIENT_IP_ADDRESS(ipaddress),
            SNAttribute.CLIENT_VERSION(version),
            SNAttribute.KEEPALIVE_DATA(
                SNAttribute.KEEPALIVE_DATA.get_keepalive_data(timestamp)),
            SNAttribute.KEEPALIVE_TIME(timestamp),
            SNAttribute.USER_NAME(username),
        ]
        super(SNThunderProtocol, self).__init__(
            code=0x3, timestamp=timestamp, attribute_list=attribute_list)


class SNRegister_Bubble(SNHeartBeat):

    def __init__(self, bubble_id, ipaddress, username, timestamp):
        attribute_list = [
            SNAttribute.CLIENT_IP_ADDRESS(ipaddress),
            SNAttribute.USER_NAME(username)
        ]
        super(SNRegister_Bubble, self).__init__(
            code=bubble_id, timestamp=timestamp, attribute_list=attribute_list)


class SNRegister_MAC(SNHeartBeat):

    """
    115.239.134.166:8000
    """

    cpu_info = 'Intel(R) Core(TM) i5-3210M CPU @ 2.50GHz'
    default_explorer = ''
    client_type = 'Mac-SingletNet'
    client_version = '1.0.1'
    memory_size = 0x00001000
    os_version = 'Mac OS X Version 10.9.5 (Build 13F1077)'
    os_lang = 'zh_CN'

    def __init__(self, username, ipaddress, mac_address='10:dd:b1:d5:95:ca'):
        attribute_list = [
            SNAttribute.USER_NAME(username),
            SNAttribute.CLIENT_VERSION(self.client_version),
            SNAttribute.CLIENT_TYPE(self.client_type),
            SNAttribute.CLIENT_IP_ADDRESS(ipaddress),
            SNAttribute.MAC_ADDRESS(mac_address),
            SNAttribute.DEFAULT_EXPLORER(self.default_explorer),
            SNAttribute.CPU_INFO(self.cpu_info),
            SNAttribute.MEMORY_SIZE(self.memory_size),
            SNAttribute.OS_VERSION(self.os_version),
            SNAttribute.OS_LANG(self.os_lang)
        ]
        super(SNRegister_MAC, self).__init__(code=0x1,
                                             timestamp=0, attribute_list=attribute_list)
        self.timeflag = 0x1


if __name__ == '__main__':
    pass
