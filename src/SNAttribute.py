#!/usr/bin/env python
# coding=utf-8
import time
import struct
import socket
import hashlib


class SNAttribute(object):

    def __init__(self, typename, parent_id, type_id, value_type, value):
        self.typename = typename
        self.parent_id = parent_id
        self.type_id = type_id
        self.value_type = value_type
        self.value = value

    @property
    def length(self):
        return len(self.value)

    def digest(self):
        fmt_str = '>BH%ds' % self.length
        return struct.pack(fmt_str, self.parent_id, self.length + 3, self.value)

    def hexdigest(self):
        return self.digest().encode('hex')


class USER_NAME(SNAttribute):

    """
    un = USER_NAME('18088888888@HYXY.XY')
    un.digest()
    """

    def __init__(self, username):
        super(USER_NAME, self).__init__(typename='User-Name',
                                        parent_id=0x1, type_id=0x0, value_type=0x2, value=username)


class CLIENT_IP_ADDRESS(SNAttribute):

    """
    cia = CLIENT_IP_ADDRESS('192.168.1.1')
    cia.digest()
    """

    def __init__(self, ipaddress):
        ipaddress = socket.inet_aton(ipaddress)
        super(CLIENT_IP_ADDRESS, self).__init__(typename='Client-IP-Address',
                                                parent_id=0x2, type_id=0x0, value_type=0x1, value=ipaddress)


class CLIENT_VERSION(SNAttribute):

    """
    cv = CLIENT_VERSION('1.2.16.20')
    cv.digest()
    """

    def __init__(self, version):
        super(CLIENT_VERSION, self).__init__(typename='Client-Version',
                                             parent_id=0x3, type_id=0x0, value_type=0x2, value=version)


class KEEPALIVE_DATA(SNAttribute):

    """
    keepalive_data = KEEPALIVE_DATA.get_keepalive_data()
    kv = KEEPALIVE_DATA(keepalive_data)
    kv.digest()
    """

    def __init__(self, keepalive_data):
        super(KEEPALIVE_DATA, self).__init__(typename='KeepAlive-Data',
                                             parent_id=0x14, type_id=0x0, value_type=0x2, value=keepalive_data)

    @classmethod
    def get_keepalive_data(cls, timestamp=int(time.time()), last_data=None):
        salt = last_data if last_data else 'test'

        m = hashlib.md5()
        m.update(struct.pack('>I', timestamp))
        m.update(salt)

        return m.hexdigest()


class KEEPALIVE_TIME(SNAttribute):

    """
    kt = KEEPALIVE_TIME(int(time.time()))
    kt.digest()
    """

    def __init__(self, timestamp):
        timestamp = struct.pack('>I', timestamp)
        super(KEEPALIVE_TIME, self).__init__(typename='KeepAlive-Time',
                                             parent_id=0x12, type_id=0x0, value_type=0x0, value=timestamp)


if __name__ == '__main__':
    pass
