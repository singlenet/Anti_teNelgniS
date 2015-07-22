import time
import copy
import struct
import hashlib


def generate_uuid(basestr='Administrator'):
    md5 = hashlib.md5(basestr)
    md5_hex = md5.hexdigest().upper()
    return '%s-%s-%s-%s' % (md5_hex[0:6], md5_hex[7:12], md5_hex[13:21], md5_hex[22:28])


class MagicNum(object):
    def __init__(self, tick=None):
        self.tick = tick or (int(time.time()) & 0x0FFFFFFFF)

    def _calc_number(self, diff_value):
        result_num = (self.tick * 0x8088405 + 1) & 0xFFFFFFFF
        return (result_num * diff_value) >> 32

    def _get_number(self, num1, num2):
        if num2 >= num1:
            return num1 + self._calc_number(num2 - num1)
        else:
            return num2 + self._calc_number(num1 - num2)

    def _second_num(self, first_num):
        num_int = [first_num / 100 % 10, first_num / 10 % 10, first_num % 10]

        result = (num_int[0] * num_int[1]) * 8
        result += (num_int[0] + num_int[1]) * 9
        result += (num_int[1] + num_int[2]) * 8
        result += (num_int[0] * num_int[2]) * 9

        return result

    def magic_number(self):
        first_num = self._get_number(101, 999)
        second_num = self._second_num(first_num)
        return int('%s%s' % (first_num, second_num))


class BaseHeartBeat(object):
    """
    ('mail.189joy.com', 8987)
    """
    _actions = {
        'login': 0xE6D2FB51,
        'keep': 0xE6D2FB52,
        'logout': 0xE6D2FB53,
        'recv_succ': 0xE6D2FB54
    }
    _fmt_str = '<llqllq28sLLlq'
    _params = {
        'head_1': 0,
        'head_2': 0,
        'timestamp': 0,
        'user_id': 0,
        'blank': 0,
        'recv_time': 0,
        'uuid': 0,
        'action': 0,
        'error': 0,
        'foot_1': 0,
        'foot_2': 0
    }

    def __init__(self, user_id=0, action='login'):
        self.user_id = user_id

        self.params = copy.copy(self._params)
        self.params['user_id'] = self.user_id
        self.params['uuid'] = generate_uuid()
        self.params['action'] = action

    def pack_data(self, recv_time=None, action='login'):
        self.params['head_1'] = MagicNum().magic_number()
        self.params['timestamp'] = int(time.time() * 1000)
        self.params['action'] = self._actions[action]
        self.params['recv_time'] = recv_time or 0

        rawdata = struct.pack(self._fmt_str,
                              self.params['head_1'],
                              self.params['head_2'],
                              self.params['timestamp'],
                              self.params['user_id'],
                              self.params['blank'],
                              self.params['recv_time'],
                              self.params['uuid'],
                              self.params['action'],
                              self.params['error'],
                              self.params['foot_1'],
                              self.params['foot_2'])
        return rawdata

    def parse_data(self, rawdata):
        params = copy.copy(self._params)
        (params['head_1'],
         params['head_2'],
         params['timestamp'],
         params['user_id'],
         params['blank'],
         params['recv_time'],
         params['uuid'],
         params['action'],
         params['error'],
         params['foot_1'],
         params['foot_2']) = struct.unpack(self._fmt_str, rawdata)
        return params


if __name__ == '__main__':
    pass