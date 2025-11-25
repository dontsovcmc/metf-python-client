# -*- coding: utf-8 -*-
import time
from requests import Session
from metf_python_client.utils import str2hex, hex2str
from metf_python_client.logger import log


class METFClient:
    def __init__(self, host, port=80, **kwargs):
        self._root = 'http://' + host + ':' + str(port)
        self._sess = Session()
        self._timeout = kwargs.get('timeout', 3.0)
        log.info('Testing: {}:{}'.format(host, port))

    def version(self):
        log.info('version')
        ret = self._sess.get(self._root + '/version', timeout=self._timeout)
        ret.raise_for_status()
        assert ret.text

    def ping(self):
        log.info('ping')
        ret = self._sess.get(self._root + '/ping', timeout=self._timeout)
        ret.raise_for_status()
        assert ret.text == 'pong'

    def pinMode(self, pin, mode):
        # INPUT, INPUT_PULLUP, OUTPUT
        log.info('set pinMode {} {}'.format(pin, mode))

        data = {'pin': pin, 'mode': mode}
        ret = self._sess.post(self._root + '/pinMode', data=data, timeout=self._timeout)
        ret.raise_for_status()
        assert ret.text == 'OK', ret.text

    def digitalRead(self, pin):
        log.info('digitalRead {}'.format(pin))

        params = {'pin': pin}
        ret = self._sess.get(self._root + '/digitalRead', params=params, timeout=self._timeout)
        ret.raise_for_status()
        assert ret.text in ['0', '1'], ret.text
        return int(ret.text)

    def digitalWrite(self, pin, value):
        log.info('digitalWrite {} {}'.format(pin, value))

        # HIGH, LOW
        data = {'pin': pin, 'value': value}
        ret = self._sess.post(self._root + '/digitalWrite', data=data, timeout=self._timeout)
        ret.raise_for_status()
        assert ret.text == 'OK', ret.text

    def delay(self, msec):
        log.info('delay {} msec'.format(msec))
        time.sleep(msec/1000.0)

    def wait_digital(self, pin, value, timeout=5.0):

        t = time.time()
        while time.time() - t < timeout and self.digitalRead(pin) != value:
            time.sleep(0.3)
        return time.time() - t < timeout

    def blynk(self, pin, duration: int = 1000, invert: bool = False, low: int = 0x0, high: int = 0x1):
        turn_on = low if invert else high
        turn_off = high if invert else low
        self.digitalWrite(pin, turn_on)
        self.delay(duration)
        self.digitalWrite(pin, turn_off)

    def i2c(self, action, **kwargs):
        data = {'action': action}
        data.update(**kwargs)

        ret = self._sess.post(self._root + '/i2c', data=data, timeout=self._timeout)
        if ret.status_code != 200:
            raise Exception('HTTP Error (' + str(ret.status_code) + '): ' + ret.text)
        return ret

    def i2c_begin(self, sda=None, scl=None):
        if sda is not None and scl is not None:
            ret = self.i2c('begin', sda_pin=sda, scl_pin=scl)
        else:
            ret = self.i2c('begin')
        assert ret.text == 'OK', ret.text

    def i2c_setClock(self, clock):
        ret = self.i2c('setClock', value=clock)
        assert ret.text == 'OK', ret.text

    def i2c_setClockStretchLimit(self, stretch):
        ret = self.i2c('setClockStretchLimit', value=stretch)
        assert ret.text == 'OK', ret.text

    def i2c_ask(self, address, message, response_len):
        hexstring = hex2str(message)  # 01FA0002
        log.info('i2c > ' + hexstring + ', wait ' + str(response_len) + ' bytes')
        ret = self.i2c('ask', address=address, hexstring=hexstring, response=response_len)
        log.info('i2c < ' + ret.text)
        return str2hex(ret.text)

    def i2c_flush(self):
        ret = self.i2c('flush')
        assert ret.text == 'OK', ret.text

    def serial_begin(self, baud: int = 115200):
        log.info('serial_begin baudrate={}'.format(baud))
        data = {'baudrate': baud}
        ret = self._sess.post(self._root + '/serial', data=data, timeout=self._timeout)
        ret.raise_for_status()

    def serial_flush(self):
        log.info('serial_flush')
        data = {'flush': '1'}
        ret = self._sess.post(self._root + '/serial', data=data, timeout=self._timeout)
        ret.raise_for_status()

    def serial_read(self):
        log.info('serial_read')
        ret = self._sess.get(self._root + '/read', timeout=self._timeout)
        ret.raise_for_status()
        return ret.text

    def serial_readlines(self,
                         wait: int = 5000,
                         delimiter: str | None = '\n',
                         prefix: str | None = '00:') \
            -> str | list[str] | None:
        """
        serial port sniffering for wait ms

        :param wait: ms timeout
        :param delimiter: separate to lines if delimiter defined
        :param prefix: merge lines if prefix defined
        :return:
        """
        d = '\\n' if delimiter == '\n' else delimiter
        log.info(f'serial_readlines wait {wait} ms, delimiter={d}, prefix={prefix}')

        t = time.time()
        out = []
        while time.time() - t < wait / 1000:
            ret = self._sess.get(self._root + '/read', timeout=self._timeout)
            ret.raise_for_status()

            if ret.text:
                if delimiter:
                    lines = ret.text.split(delimiter)
                    for line in lines:
                        if line.startswith(prefix) or not out:
                            out.append(line)
                        else:
                            out[-1] += line
                    return out
                else:
                    return ret.text

            time.sleep(0.5)
