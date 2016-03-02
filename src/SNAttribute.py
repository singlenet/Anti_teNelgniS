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

    def __init__(self, client_ip_address):
        client_ip_address = socket.inet_aton(client_ip_address)
        super(CLIENT_IP_ADDRESS, self).__init__(typename='Client-IP-Address',
                                                parent_id=0x2, type_id=0x0, value_type=0x1, value=client_ip_address)


class CLIENT_VERSION(SNAttribute):

    """
    cv = CLIENT_VERSION('1.2.16.20')
    cv.digest()
    """

    def __init__(self, client_version):
        super(CLIENT_VERSION, self).__init__(typename='Client-Version',
                                             parent_id=0x3, type_id=0x0, value_type=0x2, value=client_version)


class CLIENT_TYPE(SNAttribute):

    """
    ct = CLIENT_TYPE('Mac-SingleNet')
    ct.digest()
    """

    def __init__(self, client_type):
        super(CLIENT_TYPE, self).__init__(typename='Client-Type',
                                          parent_id=0x4, type_id=0x0, value_type=0x2, value=client_type)


class OS_VERSION(SNAttribute):

    """
    ov = OS_VERSION('Microsoft Windows XP Service Pack 3')
    ov.digest()
    """

    def __init__(self, os_version):
        super(OS_VERSION, self).__init__(typename='OS-Version',
                                         parent_id=0x5, type_id=0x0, value_type=0x2, value=os_version)


class OS_LANG(SNAttribute):

    """
    ol = OS_LANG('Chinese-RPC')
    ol.digest()
    """

    def __init__(self, os_lang):
        super(OS_LANG, self).__init__(typename='OS-Lang',
                                      parent_id=0x6, type_id=0x0, value_type=0x2, value=os_lang)


class CPU_INFO(SNAttribute):

    """
    ci = CPU_INFO('Intel(R) Core(TM) i5-3210M CPU @ 2.50GHz')
    ci.digest()
    """

    def __init__(self, cpu_info):
        super(CPU_INFO, self).__init__(typename='CPU-Info',
                                       parent_id=0x8, type_id=0x0, value_type=0x2, value=cpu_info)


class MAC_ADDRESS(SNAttribute):

    """
    ma = MAC_ADDRESS('10:dd:b1:d5:95:ca')
    ma.digest()
    """

    def __init__(self, mac_address):
        super(MAC_ADDRESS, self).__init__(typename='MAC-Address',
                                          parent_id=0x9, type_id=0x0, value_type=0x2, value=mac_address)


class MEMORY_SIZE(SNAttribute):

    """
    mz = MEMORY_SIZE(0x000001FF)
    mz.digest()
    """

    def __init__(self, memory_size):
        memory_size = struct.pack('>I', memory_size)
        super(MEMORY_SIZE, self).__init__(typename='Memory-Size',
                                          parent_id=0xa, type_id=0x0, value_type=0x0, value=memory_size)


class DEFAULT_EXPLORER(SNAttribute):

    """
    de = DEFAULT_EXPLORER('IE 6.0.2900.5512')
    de.digest()
    """

    def __init__(self, default_explorer):
        super(DEFAULT_EXPLORER, self).__init__(typename='Default-Explorer',
                                               parent_id=0xb, type_id=0x0, value_type=0x2, value=default_explorer)


class KEEPALIVE_DATA(SNAttribute):
    last_data = None

    """
    keepalive_data = KEEPALIVE_DATA.get_keepalive_data()
    kv = KEEPALIVE_DATA(keepalive_data)
    kv.digest()
    """

    def __init__(self, keepalive_data):
        super(KEEPALIVE_DATA, self).__init__(typename='KeepAlive-Data',
                                             parent_id=0x14, type_id=0x0, value_type=0x2, value=keepalive_data)

    @classmethod
    def get_keepalive_data(cls, timestamp=None):
        timestamp = timestamp or int(time.time())
        salt = cls.last_data or 'wxgj'

        m = hashlib.md5()
        m.update(struct.pack('>I', timestamp))
        m.update(salt)

        cls.last_data = keepalive_data = m.hexdigest()
        return keepalive_data


class KEEPALIVE_TIME(SNAttribute):

    """
    kt = KEEPALIVE_TIME(int(time.time()))
    kt.digest()
    """

    def __init__(self, keepalive_time):
        keepalive_time = struct.pack('>I', keepalive_time)
        super(KEEPALIVE_TIME, self).__init__(typename='KeepAlive-Time',
                                             parent_id=0x12, type_id=0x0, value_type=0x0, value=keepalive_time)


if __name__ == '__main__':
    pass
