# -*- coding: utf-8 -*-
#!/usr/bin/python

from bases.FrameworkServices.SimpleService import SimpleService
import speedtest
import os

ORDER = [
    'speedtest',
]

CHARTS = {
    'speedtest': {
        'options': [None, 'speedtest-title', 'MBit/s', 'speed test', 'speed', 'line'],
        'lines': [
            ['download'],
            ['upload']
        ]
    }
}
_https_proxy_name = 'https_proxy'
_http_proxy_name = 'http_proxy'


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):

        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.upload = self.configuration.get('upload') or 1
        self.download = self.configuration.get('download') or 1
        self.proxy = self.configuration.get('proxy') or False
        self._speed = speedtest.Speedtest(secure=True)
        _ = self._speed.best

    def check(self):
        """
        Checks module
        :return: bool
        """
        return True

    def _get_data(self):
        hsproxy = os.getenv(_https_proxy_name)
        hproxy = os.getenv(_http_proxy_name)
        ret = {}
        try:
            if self.proxy is False:
                os.environ['https_proxy'] = ''
                os.environ['http_proxy'] = ''
            else:
                os.environ['https_proxy'] = hsproxy
                os.environ['http_proxy'] = hproxy
            if self.upload:
                upbits = self._speed.upload()
                ret['upload'] = upbits / 1000.0 / 1000.0
            if self.download:
                dlbits = self._speed.download()
                ret['download'] = dlbits / 1000.0 / 1000.0
        except Exception:
            return None
        return ret


if __name__ == '__main__':
    s = speedtest.Speedtest(secure=True)
    s.download()
    s.results.json()
