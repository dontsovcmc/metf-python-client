
# ESP32-C6-Super-Mini Pin Mapping
# https://www.espressif.com/sites/default/files/documentation/esp32-c6_datasheet_en.pdf
# GPIO Pin Mapping for ESP32-C6-Super-Mini board

HIGH = 0x1
LOW = 0x0

INPUT = 0x01
INPUT_PULLUP = 0x05
OUTPUT = 0x03


# Digital I/O Pins
GPIO0 = 0   # Strapping pin, ADC, Boot button
GPIO1 = 1   # Strapping pin, ADC
GPIO2 = 2   # ADC
GPIO3 = 3   # ADC, Strapping pin
GPIO4 = 4   # ADC, JTAG
GPIO5 = 5   # ADC, JTAG
GPIO6 = 6   # ADC, JTAG
GPIO7 = 7   # ADC, JTAG

GPIO8 = 8   # Strapping pin
GPIO9 = 9   # Boot mode control (strapping pin)

GPIO10 = 10 # Digital I/O
GPIO11 = 11 # Digital I/O
GPIO12 = 12 # Digital I/O
GPIO13 = 13 # Digital I/O
GPIO14 = 14 # Digital I/O
GPIO15 = 15 # Digital I/O, Built-in LED on Super Mini

GPIO16 = 16 # UART0 RX (USB serial)
GPIO17 = 17 # UART0 TX (USB serial)

GPIO18 = 18 # Digital I/O
GPIO19 = 19 # Digital I/O
GPIO20 = 20 # Digital I/O, USB D-
GPIO21 = 21 # Digital I/O, USB D+
GPIO22 = 22 # Digital I/O
GPIO23 = 23 # Digital I/O

# UART pins
UART_TX = GPIO17
UART_RX = GPIO16

# I2C pins (commonly used, configurable)
SDA = GPIO6  # Default I2C SDA
SCL = GPIO7  # Default I2C SCL

# SPI pins (commonly used, configurable)
MOSI = GPIO4  # Default SPI MOSI
MISO = GPIO5  # Default SPI MISO
SCK = GPIO6   # Default SPI SCK
CS = GPIO7    # Default SPI CS

# Built-in LED
LED_BUILTIN = GPIO15

# ADC capable pins
# GPIO0, GPIO1, GPIO2, GPIO3, GPIO4, GPIO5, GPIO6, GPIO7

# Special pins
BOOT = GPIO9  # Boot mode pin
FLASH_BUTTON = GPIO0  # Usually connected to boot button
