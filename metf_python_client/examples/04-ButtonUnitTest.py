# -*- coding: utf-8 -*-
import unittest
from metf_python_client import METFClient
from metf_python_client.boards.nodemcu import D5, LOW, HIGH, INPUT_PULLUP


ESP_HOST = '192.168.3.49'


class TestMethods(unittest.TestCase):

    def test_button(self):
        # Wait You press button
        # https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/
        api = METFClient(ESP_HOST)

        api.pinMode(D5, INPUT_PULLUP)

        # check D5 is HIGH
        self.assertEqual(api.digitalRead(D5), HIGH)

        # 3 seconds for press button
        self.assertTrue(api.wait_digital(D5, LOW, 3.0), "Button wasn't pressed")


if __name__ == '__main__':
    unittest.main()
