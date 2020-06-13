# -*- coding: utf-8 -*-
from metf_python_client import METFClient, LOW, HIGH, INPUT
from metf_python_client.boards.nodemcu import D2, D3, D4, D6, D7
from metf_python_client import log

from requests.exceptions import HTTPError

ESP_HOST = '192.168.3.46'


def test_i2c(host):
    try:
        api = METFClient(host)

        api.pinMode(D2, INPUT)

        # Сигнал о пробуждении устройства
        assert api.wait_digital(D2, HIGH, 5.0)

        api.delay(20)

        # Поехали общаться
        api.i2c_begin(0, 2)
        api.i2c_setClock(100000)
        api.i2c_setClockStretchLimit(1500)

        addr = 10

        ret = api.i2c_ask(addr, 'M', 1)  # 'M'  mode

        ret = api.i2c_ask(addr, 'B', 10)  # 'B'  get data

    except HTTPError as err:
        log.error(err.response.text)
        raise Exception(err.response.text)


test_i2c(ESP_HOST)
