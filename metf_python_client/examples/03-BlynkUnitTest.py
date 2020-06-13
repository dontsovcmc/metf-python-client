# -*- coding: utf-8 -*-
import unittest
from metf_python_client import METFClient, HIGH, LOW, OUTPUT
from metf_python_client.boards.nodemcu import LED_BUILTIN_AUX


ESP_HOST = '192.168.3.49'


class TestMethods(unittest.TestCase):

    def test_blynk(self):
        # Blynk build id NodeMCU LED
        # https://lowvoltage.github.io/2017/07/09/Onboard-LEDs-NodeMCU-Got-Two
        api = METFClient(ESP_HOST)

        pin = LED_BUILTIN_AUX

        api.pinMode(pin, OUTPUT)

        api.digitalWrite(pin, LOW)
        api.delay(1000)
        api.digitalWrite(pin, HIGH)


if __name__ == '__main__':
    unittest.main()
