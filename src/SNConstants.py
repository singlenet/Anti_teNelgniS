#!/usr/bin/env python
# coding=utf-8
import base64

NKAccount = {
    'SHARE_KEY': base64.decodestring('emp4aW5saXN4MDE=')
}

SNAccount = {
    'SHARE_KEY': base64.decodestring('c2luZ2xlbmV0MDE=')
}

SNClient = {
    'CLIENT_VERSION': '1.2.16.20',
    'CLIENT_TYPE': base64.decodestring('c2luZ2xlTmV0')
}

HBDefault = {
    'SIG_SALT': base64.decodestring('TExXTFhB'),
    'ADAPTER_INFO': 'AMD PCNET Family PCI Ethernet Adapter - 数据包计划程序微型端口',
    'DEFAULT_EXPLORER': 'IE 6.0.2900.5512',
    'MEMORY_SIZE': 0x000001FF,
    'MAC_ADDRESS': '00-0C-29-F1-51-37',
    'CPU_INFO': 'Intel(R) Core(TM) i5-3210M CPU @ 2.50GHz',
    'OS_LANG': 'Chinese-RPC',
    'OS_VERSION': 'Microsoft Windows XP Service Pack 3'
}
