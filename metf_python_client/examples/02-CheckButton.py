# -*- coding: utf-8 -*-
from metf_python_client import METFClient, LOW, HIGH, INPUT_PULLUP
from metf_python_client.boards.nodemcu import D5


ESP_HOST = '192.168.3.49'


def test_button(host):
    # Wait You press button
    # https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/
    api = METFClient(host)

    api.pinMode(D5, INPUT_PULLUP)
    assert api.digitalRead(D5) == HIGH
    assert api.wait_digital(D5, LOW, 3.0), "Button wasn't pressed"


test_button(ESP_HOST)
