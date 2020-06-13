# -*- coding: utf-8 -*-
from metf_python_client import METFClient, HIGH, LOW, OUTPUT
from metf_python_client.boards.nodemcu import LED_BUILTIN_AUX


ESP_HOST = '192.168.3.49'


def blynk(host):
    # Blynk build id NodeMCU LED
    # https://lowvoltage.github.io/2017/07/09/Onboard-LEDs-NodeMCU-Got-Two

    api = METFClient(host)

    pin = LED_BUILTIN_AUX

    api.pinMode(pin, OUTPUT)
    api.digitalWrite(pin, LOW)

    assert api.digitalRead(pin) == LOW

    api.delay(1000)
    api.digitalWrite(pin, HIGH)

    assert api.digitalRead(pin) == HIGH


blynk(ESP_HOST)
