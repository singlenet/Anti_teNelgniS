import json
import requests
from requests.utils import quote
from LongBase64 import LongBase64


class LoginFailed(Exception):
    pass


class RequestVpnFailed(Exception):
    pass


class STLogin(object):
    _headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Trident/4.0) STBrowser/4.0.1.2',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    _vpn_params = {
        'st': 'username=%s&password=%s&flashInfo=%s'
    }
    _login_uri = 'http://member.189joy.com/checkLogin/login.do'
    _vpn_uri = 'http://vpn.189joy.com/AssignVpn/assignVpn.do'


    def __init__(self, username):
        self.username = username
        self.s = requests.Session()
        self.s.headers = self._headers

    def do_login(self, password):
        lb64 = LongBase64()
        logininfo = '%s|%s|122.227.254.206|8988|1|4.0.1.2' % (self.username, password)
        logininfo = lb64.encodestring(logininfo)
        postdata = quote(logininfo)

        login_resp = self.s.post(self._login_uri, data={'logininfo': postdata})
        login_res = json.loads(login_resp.content)
        if login_res['r'] != 1:
            raise LoginFailed('Login Failed: %s' % login_res['err_msg'])
        self.user = login_res
        return True, login_res

    def request_vpn(self):
        if not self.user:
            raise RequestVpnFailed('Not Login yet.')
        lb64 = LongBase64()
        vpnparams = 'username=%s&password=%s&flashInfo=%s' % (
            self.user['stcode'], self.user['userpassword'], self.user['sxcode'])
        postdata = quote(vpnparams)

        vpn_resp = self.s.post(self._vpn_uri, params={'st': postdata})
        return lb64.decodestring(vpn_resp.content)


if __name__ == '__main__':
    pass