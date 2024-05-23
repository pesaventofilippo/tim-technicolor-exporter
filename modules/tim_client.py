import re
import time
import hashlib
import requests


class TimModemAPI:
    def __init__(self, router_ip: str, username: str, password: str):
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self._session = requests.Session()
        self._last_down = 0
        self._last_up = 0
        self._down_offset = 0
        self._up_offset = 0
        self.FIRST_RUN = True

    def login(self):
        preauth_data = self._session.get(f"http://{self.router_ip}/login.lp?get_preauth=true")
        rn, realm, nonce, qop = preauth_data.text.split('|')

        HA1 = hashlib.md5(f"{self.username}:{realm}:{self.password}".encode()).hexdigest()
        HA2 = hashlib.md5('GET:/login.lp'.encode()).hexdigest()
        hidepw = hashlib.md5(f"{HA1}:{nonce}:00000001:xyz:{qop}:{HA2}".encode()).hexdigest()

        login_data = {
            'rn': rn,
            'hidepw': hidepw,
            'user': self.username
        }

        self._session.post(f"http://{self.router_ip}/login.lp", data=login_data)

    @staticmethod
    def _bytes_delta(_bytes: int, _last: int) -> int:
        if _bytes < _last:
            return 4 * (1024 ** 3) - _last + _bytes
        return _bytes - _last

    def _get_internet_raw(self, _retrycount: int=0) -> (int, int):
        try:
            res = self._session.get(f"http://{self.router_ip}/network-expert-internet.lp?ip=&phoneType=undefined")
            pattern = r'userfriendlydisplay1\("([^"]+)"\)'
            up, down = re.findall(pattern, res.text)
            return int(down), int(up)
        except Exception:
            if _retrycount < 3:
                time.sleep(0.2)
                self.login()
                return self._get_internet_raw(_retrycount+1)
            else:
                raise

    def get_internet_delta(self) -> (int, int):
        down, up = self._get_internet_raw()

        if self.FIRST_RUN:
            self._down_offset = down
            self._up_offset = up
            self.FIRST_RUN = False

        down_delta = self._bytes_delta(down, self._last_down)
        up_delta = self._bytes_delta(up, self._last_up)

        self._last_down, self._last_up = down, up
        return down_delta - self._down_offset, up_delta - self._up_offset
