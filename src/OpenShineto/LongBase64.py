import time
import base64


class LongBase64(object):
    """
    usage:
        lb64 = LongBase64()
        lb64.Long_EnCode(string)
        lb64.Long_DeCode(encode_string)
    """
    _encrypt_seed_1 = [
        'salku!doew%oi3ry*khasl$kjf#gdksh',
        'pjf/726;lsjfgo^s9234khsldfk:lkjl',
        'klu\owe8*6>sjdhf8yi6,+-!ksdfh@19',
        '834k|hdf3yg><mhyo5eyr850*7&sdfy*',
        '239847jkeyGdjlHoiysdfAV68435*^%B',
        'sjdfyh28345&&^*&%kjhkUTIUGI87tsd',
        'Kiyu98a98&%:{{}POsjfhwe87s5sudf@',
        'ksdhyf&^&hfs9JKhskdfu(*fdfljgURF',
        's^dfh7KL8kjsdfg(ishdfo*&)kjhdsfi',
        'uiyewrYODf98jUOI(*{LJOIewyjksd88',
        'wjeyruUYIU*^87t58klY*7ulkdfoiw3s',
        'sdyf8923tuihsodfiyho&(*of;lous0L',
        'oiyr0239798YGHguiwyeifuowie0*&(*',
        'skldfuo2y3723igYTUfweuoy)*&*9woL',
        '2384hfrw)(4H08ogh9E8R;{K;FSLEFds',
        '&*^^RIbfdisuJHKgh{}f;kisydf(*^kj',
        'sldfIYO7(*TY(&OUGisfdjhO;,.,sdf8',
        '2398YIUHOeyf98y)*(whpiudfKJHUYfs',
        'skdujfoi8Y(*yfshowueflhOY(*PO:Lh',
        'woiye9823hugsdfbflHFOefb)(&(*Yfw',
        'wsrfiwoeyh98Y(fwofbnhd:K;lmflk&k',
        'sodf(&^(&foigf7y979nhsofuIUFBosh',
        'adfy8^(f39o47tsdfosughfFHiusdfu*',
        '(*^foiwhf&FGowefhowf(98sdf*)&fwh',
        'saihfoY&(*F929uofGOF98f6ysify98Y',
        'OIYHf8(^(7687wsfljYfuswfdown80y7',
        'oisfy89y(*YFwhe20(**&%$#)(&(sdfD',
        '897%$E198767HI^&^6576sdfhwoe~sdg',
        'skdfh^*&Tfbwft9hOYF98:.,mkpo,OIJ',
        '!kjhgsdf645&^%&^97E#$%shfsfouHO6',
        'sjdfhuITY&Fhuowegf8gHYVYfsjdhfkh']
    _encrypt_seed_2 = [
        "dyfw9y87T*&TfwboY(*Y87ft23nbouHf",
        "^23ioyO*9ywoiej98_(*)mjoifwehHU9",
        "wehroY(Y9f7h1276oiwe%^sdfa*&8j2o",
        "8967UH78fhwyegf6rts67df*&Y&(hywe",
        "akshfy9876Y&876tiwheyt^*Yuhwuef}",
        "*^&(*Fhu298njsoldfhPJIOwdug([}$4",
        "sakldf*T*uhwyefgIYIh9798yIH*97*^",
        "~soidfu98Y&Tfyiwge6*&^(*&HUOkjfO",
        "876HUIGyiosyu9f8s(*U)J809sjfi*Y&",
        "sadfh9*^&fyhgy82trysfuydgft6%*^N",
        "23947h&Gfyigtfiweut^*T*08njsihi^",
        "iu*&(GH~@jhkjh!iof9JP[]{:{ojonhy",
        "oHY*Y&y786(&Jy708jIHYIToiu89&IJ}",
        "\|iou8y(*^&T^IUH&^&HOUH(*uisgf3i",
        "*(&ondfiy&|};pJKOIHi,.kmihj?/&^j",
        "sdifh98Y&H;:oju8&H&^RTVUF(]|hyih",
        "/(^ghiweyg87bfldsij*JMonjh><Opo7",
        "ksjdf876UG*YG09JIOH_+-p.,/?juoiw",
        "(&Unjosufh&YIbifgsjd989yHI4$^5hs",
        "*U)*jfuosy9T^GIYfgysJHGTy6trGU(8",
        "skldfhiOY&(*houhsdft68TBVgufvLJ,",
        "(*&98fhwoudhyw7hg&GBiyhbweuy&^g~",
        "IUOi8f98uuh&T^*YHG;,+=-0=skdinug",
        "897osdhoUY(*Hnofnwhigi:M:op9{ki3",
        "sidfhy98YHGyf7sr8iPK_(*&YY;:M>m+",
        "(8oisndfht*^&RT^&bubdsolhn;Pmlkm",
        "OI&*(hf87tgfkU!`09ujo$ksfjh*(jou",
        "09u*)IJHsoidh{L}\m;lmweo89JL,:\/",
        "IU(*7yfc98wh8t^*HBOHfwsdnfiuy)ko",
        "*(&(*houhsyibgsiyt976t8H)OJP:[<M",
        "sdijfhoy8(*Y*&g86r7Bigi8olhIUln@"]
    _random_num = None

    def _decode_num(self, num):
        opt_num = int(num)
        re = (opt_num / 3 - 2046) / 8 + 19970701
        re = '%d' % re
        if len(re) == 8:
            return re[-4:]

    def _get_value_insert(self, ym):
        today = ym
        int_mon = int(today[0:2])
        int_day = int(today[2:4])

        if int_mon > 12 or int_day > 31:
            return None
        if int_mon < 1 or int_day < 1:
            return None

        seed_1 = self._encrypt_seed_1[int_day - 1]
        seed_2 = self._encrypt_seed_2[abs(30 - int_day)]

        i = abs(int_day - 2 * int_mon)
        if i == 0:
            i = int_mon
        s1_len = len(seed_1)
        s2_len = len(seed_2)

        if int_mon % 2 == 0:
            s1_pos = seed_1[0: i]
            s2_pos = seed_2[int_mon - 1: 2 * int_mon - 1]
        else:
            s1_pos = seed_1[s1_len - i: s1_len]
            s2_pos = seed_2[int_mon - 1: 2 * int_mon - 1]

        tmp_str = s2_pos + s1_pos

        value_insert = ''
        for c in tmp_str:
            if ord(c) >= 48 and ord(c) <= 57:
                j = int(c) % s2_len
            else:
                j = ord(c) % s2_len
            if j == 0:
                j = 5
            value_insert = value_insert + seed_2[j - 1]

        if int_day <= 15:
            i = 15 - int_day
            if i == 0:
                i = 7
            j = int_mon
            if j < 6:
                j += 3
            if int_day % 2 == 0:
                value_insert = value_insert + seed_2[0: i] + seed_2[s2_len - j: s2_len]
            else:
                value_insert = value_insert + seed_1[0: 15 - int_day] + seed_1[s1_len - int_day: s1_len]
        else:
            i = int_day % 9
            if i == 0:
                i = 9
            j = int_mon
            if j < 6:
                j += 4

            if int_day % 2 == 0:
                value_insert = value_insert + seed_2[s2_len - i: s2_len] + seed_1[0: j]
            else:
                value_insert = value_insert + seed_1[s2_len - i: s2_len] + seed_2[0: j]

        return value_insert

    def _string_of_char(self, char, times):
        return char * times

    def _do_output(self, a_str, b_str):
        base = base64.decodestring(a_str)

        base_len = len(base)
        b_len = len(b_str)
        r = ''

        if base_len >= b_len:
            diff = base_len - b_len
            tmp_str = b_str + self._string_of_char(b_str[0], diff)

            for i in xrange(base_len):
                r = r + chr((ord(base[i]) ^ ord(tmp_str[i])))
        else:
            for i in xrange(base_len):
                r += chr(ord(base[i]) ^ ord(b_str[i]))

        res = base64.decodestring(r)

        return res

    def _get_random(self):
        self._random_num = int(time.time()) & 0x0FFFFFFF
        self._random_num = 95394635
        re = {}

        def calc_number(diff_value):
            self._random_num = self._random_num * 0x8088405 + 1
            self._random_num = self._random_num & 0xFFFFFFFF
            return (self._random_num * diff_value) >> 32

        def get_number(num1, num2):
            if num2 >= num1:
                return num1 + calc_number(num2 - num1)
            else:
                return num2 + calc_number(num1 - num2)

        re['year'] = get_number(1998, 9999)
        re['month'] = get_number(1, 12)
        re['day'] = get_number(1, 29)

        return re

    def _en_num(self, num):
        opt_num = int(num)
        re = ((opt_num - 19970701) * 8 + 2046) * 3
        return '%d|' % re

    def _do_insert(self, a_str, b_str):
        a_len = len(a_str)
        b_len = len(b_str)
        res = ''

        if a_len > b_len:
            diff = a_len - b_len
            t_replay = b_str[0]
            tmp_str = b_str + self._string_of_char(t_replay, diff)

            for i in xrange(a_len):
                res += chr(ord(a_str[i]) ^ ord(tmp_str[i]))
        else:
            for i in xrange(a_len):
                res += chr(ord(a_str[i]) ^ ord(b_str[i]))

        res = base64.encodestring(res)
        res = res.replace('\n', '')

        return res

    def encodestring(self, plaintext):
        r_time = self._get_random()

        mon = '%02d' % r_time['month']
        day = '%02d' % r_time['day']

        mmdd = mon + day
        value_insert = self._get_value_insert(mmdd)

        base_str = base64.encodestring('%s$LONGMIMASPLIT$%d' % (plaintext, int(time.time() * 1000)))
        base_str = base_str.replace('\n', '')

        new_string = self._do_insert(base_str, value_insert)
        new_string = self._en_num('%d%s' % (r_time['year'], mmdd)) + new_string

        return new_string

    def decodestring(self, ciphertext):
        tmp = ciphertext.split('|')
        deCode = self._decode_num(tmp[0])

        value_insert = self._get_value_insert(deCode)
        new_string = self._do_output(tmp[1], value_insert)

        new_string = new_string.split('$LONGMIMASPLIT$')
        return new_string[0]


if __name__ == '__main__':
    pass