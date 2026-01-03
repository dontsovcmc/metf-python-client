# -*- coding: utf-8 -*-
from metf_python_client import METFClient
from time import sleep

ESP_HOST = '192.168.51.14'


def blynk_rgb(host):
    # Blynk by buildin RBG LED on ESP32-C6 Super-mini board

    api = METFClient(host)

    api.rgb_begin()
    api.rgb_brightness(255)
    api.rgb_color('FF0000')  # red color
    sleep(0.3)
    api.rgb_brightness(10)
    api.rgb_color('00FF00')  # green color
    sleep(0.3)
    api.rgb_brightness(200)
    api.rgb_color('0000FF')  # blue color
    sleep(0.3)
    api.rgb_brightness(0)


blynk_rgb(ESP_HOST)
