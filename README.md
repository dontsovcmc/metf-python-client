# METF Python Client

[![PyPI version](https://badge.fury.io/py/metf-python-client.svg)](https://badge.fury.io/py/metf-python-client)
[![Python Versions](https://img.shields.io/pypi/pyversions/metf-python-client.svg)](https://pypi.org/project/metf-python-client/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/metf-python-client)](https://pepy.tech/project/metf-python-client)

**HTTP client library for testing hardware using ESP boards (NodeMCU, WeMos, ESP32C6)**

Test your embedded hardware through HTTP requests. Perfect for Continuous Integration in hardware development.

---

## Features

- **Digital I/O Control**: pinMode, digitalRead, digitalWrite operations
- **I2C Communication**: Full I2C master support (begin, ask, setClock, setClockStretchLimit)
- **Serial Port Sniffing**: Read and monitor serial output from connected devices
- **RGB LED Control**: Control RGB LEDs connected to ESP boards
- **Multiple Board Support**: NodeMCU, WeMos D1 Mini, ESP32C6 Super Mini
- **Simple HTTP API**: Test hardware from any language/platform that supports HTTP
- **Hardware CI/CD**: Integrate hardware tests into your continuous integration pipeline

---

## Installation

```bash
pip install metf-python-client
```

---

## Quick Start

### 1. Setup Hardware
1. Connect your MCU/device to an ESP board (NodeMCU, WeMos, or ESP32C6)
2. Flash [METF firmware](https://github.com/dontsovcmc/metf) to the ESP board
3. Connect ESP to your network (note its IP address)

### 2. Write Test Script

```python
from metf_python_client import METFClient
from metf_python_client.boards.nodemcu import LED_BUILTIN_AUX, HIGH, LOW, OUTPUT

# Connect to ESP board
api = METFClient('192.168.1.100')

# Test connectivity
api.ping()  # Returns 'pong'

# Control GPIO
pin = LED_BUILTIN_AUX
api.pinMode(pin, OUTPUT)
api.digitalWrite(pin, LOW)
assert api.digitalRead(pin) == LOW

api.delay(1000)
api.digitalWrite(pin, HIGH)
assert api.digitalRead(pin) == HIGH
```

---

## API Reference

### Connection

```python
from metf_python_client import METFClient

# Connect to ESP board
api = METFClient(host='192.168.1.100', port=80, timeout=3.0)

# Test connection
api.ping()  # Returns 'pong' if successful
```

### Digital I/O

```python
from metf_python_client.boards.nodemcu import D1, D2, D3, INPUT, OUTPUT, INPUT_PULLUP, HIGH, LOW
from metf_python_client import METFClient

api = METFClient("192.168.1.2")  # nodemcu active point with METF firmware

# Set pin mode
api.pinMode(D1, OUTPUT)
api.pinMode(D2, INPUT)
api.pinMode(D3, INPUT_PULLUP)

# Write digital value
api.digitalWrite(D1, HIGH)
api.digitalWrite(D1, LOW)

# Read digital value
value = api.digitalRead(D2)  # Returns 0 or 1

# Wait for specific value (with timeout)
button_pressed = api.wait_digital(D2, LOW, timeout=5.0)
if button_pressed:
    print("Button was pressed within 5 seconds")
```

### I2C Communication

```python
from metf_python_client.boards.nodemcu import D3, D4

# Initialize I2C (default pins)
api.i2c_begin()  # Use default SDA/SCL for your board

# OR initialize with custom pins
api.i2c_begin(sda=D3, scl=D4)

# Set clock speed
api.i2c_setClock(400000)  # 400kHz

# Set clock stretch limit (ESP8266 specific)
api.i2c_setClockStretchLimit(1500)

# Send message and receive response
slave_address = 0x48
message = 'M'  # Send byte 0x4D
response_length = 1
response = api.i2c_ask(slave_address, message, response_length)
print(f"Received: {ord(response[0])}")

# Flush I2C buffer
api.i2c_flush()
```

#### Working with Binary Data

```python
from metf_python_client.utils import DataStruct

# Define structure format
fields = [
    ('version',      'B'),  # unsigned char
    ('value_uint16', 'H'),  # unsigned short
    ('value_uint32', 'L'),  # unsigned long
]

# Calculate structure size
header_len = DataStruct.calcsize(fields)

# Read from I2C device
response = api.i2c_ask(slave_address, 'A', header_len)

# Parse binary data
header = DataStruct(fields, response)
print(f"Version: {header.version}")
print(f"Value 16: {header.value_uint16}")
print(f"Value 32: {header.value_uint32}")
```

### Serial Port Sniffing

```python
# Initialize serial port
api.serial_begin(baudrate=115200)

# Read available data
data = api.serial_read()  # Returns string or empty string
if data:
    print(f"Received: {data}")

# Read lines with timeout and parsing
lines = api.serial_readlines(
    wait=5000,        # Wait up to 5000ms
    delimiter='\n',   # Split by newline
    prefix='00:'      # Merge lines starting with this prefix
)

for line in lines:
    print(f"Line: {line}")

# Flush serial buffer
api.serial_flush()
```

### RGB LED Control

```python
# Initialize RGB LED
api.rgb_begin()

# Set brightness (0-255)
api.rgb_brightness(128)

# Set color (hex string)
api.rgb_color('FF0000')  # Red
api.rgb_color('00FF00')  # Green
api.rgb_color('0000FF')  # Blue
api.rgb_color('FFFFFF')  # White
```

### Utility Functions

```python
# Blink LED
api.blynk(
    pin=LED_BUILTIN,
    duration=1000,   # Duration in milliseconds
    invert=False,    # Invert logic (for active-low LEDs)
    low=0,           # Low value
    high=1           # High value
)

# Delay
api.delay(1000)  # Delay 1000ms (1 second)
```

---

## Board Pin Definitions

Import board-specific pin mappings and constants:

### NodeMCU

```python
from metf_python_client.boards.nodemcu import (
    D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10,
    LED_BUILTIN, LED_BUILTIN_AUX,
    HIGH, LOW,
    INPUT, OUTPUT, INPUT_PULLUP
)
```

### WeMos D1 Mini

```python
from metf_python_client.boards.wemos import (
    D0, D1, D2, D3, D4, D5, D6, D7, D8,
    LED_BUILTIN,
    HIGH, LOW,
    INPUT, OUTPUT, INPUT_PULLUP
)
```

### ESP32C6 Super Mini

```python
from metf_python_client.boards.esp32c6_super_mini import (
    IO0, IO1, IO2, IO3, IO4, IO5, IO6, IO7, IO8, IO9, IO10,
    IO11, IO12, IO13, IO15, IO18, IO19, IO20, IO21, IO22, IO23,
    LED_BUILTIN,
    HIGH, LOW,
    INPUT, OUTPUT, INPUT_PULLUP
)
```

---

## Examples

Complete examples are available in the [examples directory](metf_python_client/examples/):

### Example 1: Blink LED

```python
from metf_python_client import METFClient
from metf_python_client.boards.nodemcu import LED_BUILTIN_AUX, OUTPUT

api = METFClient('192.168.1.100')
api.pinMode(LED_BUILTIN_AUX, OUTPUT)

# Blink LED
api.blynk(LED_BUILTIN_AUX, duration=1000)
```

### Example 2: Check Button Press

```python
from metf_python_client import METFClient
from metf_python_client.boards.nodemcu import D5, INPUT_PULLUP, LOW

api = METFClient('192.168.1.100')
api.pinMode(D5, INPUT_PULLUP)

# Wait for button press (3 second timeout)
if api.wait_digital(D5, LOW, 3.0):
    print("Button pressed!")
else:
    print("Timeout - button not pressed")
```

### Example 3: I2C Communication

```python
from metf_python_client import METFClient
from metf_python_client.boards.nodemcu import D3, D4

api = METFClient('192.168.1.100')
api.i2c_begin(D3, D4)

# Send command and receive response
slave_address = 0x48
message = '\x00'  # Read register 0x00
response = api.i2c_ask(slave_address, message, 2)

print(f"Received {len(response)} bytes")
```

### Example 4: RGB LED

```python
from metf_python_client import METFClient

api = METFClient('192.168.1.100')
api.rgb_begin()
api.rgb_brightness(100)

# Cycle through colors
colors = ['FF0000', '00FF00', '0000FF', 'FFFF00', 'FF00FF', '00FFFF']
for color in colors:
    api.rgb_color(color)
    api.delay(1000)
```

More examples:
- [01-Blynk.py](metf_python_client/examples/01-Blynk.py) - Blink onboard LED
- [02-CheckButton.py](metf_python_client/examples/02-CheckButton.py) - Button press detection
- [03-BlynkUnitTest.py](metf_python_client/examples/03-BlynkUnitTest.py) - Unit test for LED
- [04-ButtonUnitTest.py](metf_python_client/examples/04-ButtonUnitTest.py) - Unit test for button
- [05-i2c.py](metf_python_client/examples/05-i2c.py) - I2C communication
- [06-RGBLed.py](metf_python_client/examples/06-RGBLed.py) - RGB LED control

---

## Use Cases

### Hardware CI/CD Pipeline

Integrate hardware tests into your continuous integration workflow:

```python
import unittest
from metf_python_client import METFClient
from metf_python_client.boards.nodemcu import D1, D2, INPUT, OUTPUT, HIGH, LOW

class HardwareTests(unittest.TestCase):
    def setUp(self):
        self.api = METFClient('192.168.1.100')

    def test_power_led(self):
        """Test that power LED is on"""
        self.api.pinMode(D1, INPUT)
        self.assertEqual(self.api.digitalRead(D1), HIGH)

    def test_button_press(self):
        """Test button press detection"""
        self.api.pinMode(D2, INPUT_PULLUP)
        pressed = self.api.wait_digital(D2, LOW, timeout=5.0)
        self.assertTrue(pressed, "Button was not pressed")

    def test_i2c_sensor(self):
        """Test I2C sensor communication"""
        self.api.i2c_begin()
        response = self.api.i2c_ask(0x48, '\x00', 2)
        self.assertEqual(len(response), 2, "Sensor not responding")

if __name__ == '__main__':
    unittest.main()
```

### Interactive Hardware Testing

Test hardware configurations interactively:

```python
from metf_python_client import METFClient

def test_voltage_levels():
    """Test device at different voltage levels"""
    voltages = [3.0, 3.3, 5.0]
    api = METFClient('192.168.1.100')

    for voltage in voltages:
        input(f"Set power supply to {voltage}V and press Enter...")
        api.i2c_begin()
        response = api.i2c_ask(0x48, '\x00', 2)

        if len(response) == 2:
            print(f"✓ {voltage}V: PASS")
        else:
            print(f"✗ {voltage}V: FAIL")

test_voltage_levels()
```

### Production Testing

Automated testing during manufacturing:

```python
from metf_python_client import METFClient
from metf_python_client.boards.nodemcu import *

def production_test(board_id):
    """Run complete production test suite"""
    api = METFClient('192.168.1.100')
    results = {}

    # Test 1: Power-on self-test
    api.pinMode(LED_BUILTIN, OUTPUT)
    api.digitalWrite(LED_BUILTIN, HIGH)
    results['led'] = api.digitalRead(LED_BUILTIN) == HIGH

    # Test 2: I2C sensors
    api.i2c_begin()
    try:
        response = api.i2c_ask(0x48, '\x00', 2)
        results['sensor'] = len(response) == 2
    except:
        results['sensor'] = False

    # Test 3: Serial communication
    api.serial_begin(115200)
    api.serial_flush()
    lines = api.serial_readlines(wait=2000, delimiter='\n')
    results['serial'] = len(lines) > 0

    # Generate report
    print(f"\n=== Board {board_id} Test Results ===")
    for test, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{test}: {status}")

    return all(results.values())

# Test multiple boards
for board_num in range(1, 11):
    if production_test(board_num):
        print(f"Board {board_num}: ✓ PASSED\n")
    else:
        print(f"Board {board_num}: ✗ FAILED - CHECK HARDWARE\n")
```

---

## Requirements

- **Python**: 3.7 or higher
- **Dependencies**: requests>=2.22.0
- **Hardware**: ESP8266/ESP32 board with [METF firmware](https://github.com/dontsovcmc/metf)

### Supported ESP Boards
- NodeMCU (ESP8266)
- WeMos D1 Mini (ESP8266)
- ESP32C6 Super Mini

---

## ESP Firmware

The ESP board runs METF firmware, which provides an HTTP API for hardware control. The firmware is based on [ESPAsyncWebServer](https://github.com/me-no-dev/ESPAsyncWebServer).

**Get the firmware**: [https://github.com/dontsovcmc/metf](https://github.com/dontsovcmc/metf)

### Firmware Features
- HTTP REST API for GPIO, I2C, Serial control
- Supports multiple ESP8266 and ESP32 boards
- Async web server for fast response times
- Easy configuration via web interface

---

## Development

### Install Development Dependencies

```bash
# Option 1: Install package with dev dependencies
pip install metf-python-client[dev]

# Option 2: Install from source with requirements_dev.txt (recommended for contributors)
git clone https://github.com/dontsovcmc/metf-python-client
cd metf-python-client
pip install -r requirements_dev.txt
pip install -e .

# Option 3: Install from source with dev dependencies
git clone https://github.com/dontsovcmc/metf-python-client
cd metf-python-client
pip install -e .[dev]
```

**Note:** `requirements_dev.txt` includes all tools needed for development, testing, code quality checks, and publishing to PyPI.

### Run Tests

```bash
pytest tests/
```

### Code Style

```bash
# Format code
black metf_python_client/

# Check style
flake8 metf_python_client/

# Type checking
mypy metf_python_client/
```

### Build and Publish

```bash
# Build package
python3 -m build

# Check build
twine check dist/*

# Publish to PyPI (maintainers only)
twine upload dist/*
```

For detailed publishing instructions, see [CONTRIBUTING.md](CONTRIBUTING.md#publishing-to-pypi).

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Keep commits atomic and well-described

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Evgeny Dontsov**
- Email: don-and-home@mail.ru
- GitHub: [@dontsovcmc](https://github.com/dontsovcmc)

---

## Links

- **PyPI**: https://pypi.org/project/metf-python-client/
- **GitHub Repository**: https://github.com/dontsovcmc/metf-python-client
- **ESP Firmware**: https://github.com/dontsovcmc/metf
- **Issue Tracker**: https://github.com/dontsovcmc/metf-python-client/issues
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

## Acknowledgments

- Based on [ESPAsyncWebServer](https://github.com/me-no-dev/ESPAsyncWebServer)
- Inspired by the need for hardware CI/CD in embedded development

---

## FAQ

### Q: Can I use this with other ESP boards?
A: Yes! As long as you flash the METF firmware, any ESP8266 or ESP32 board should work. You may need to create custom pin definitions for your specific board.

### Q: How do I find the IP address of my ESP board?
A: Check your router's DHCP client list, use a network scanner, or configure the ESP with a static IP in the firmware.

### Q: Can I control multiple ESP boards from one script?
A: Yes! Just create multiple `METFClient` instances with different IP addresses.

```python
esp1 = METFClient('192.168.1.100')
esp2 = METFClient('192.168.1.101')
```

### Q: What's the difference between METF and direct ESP programming?
A: METF allows you to control hardware remotely via HTTP, making it perfect for automated testing and CI/CD. No need to flash new firmware for each test - just write Python scripts!

### Q: Can I use this in production devices?
A: METF is designed for testing and development. For production, consider direct firmware implementation for better security and performance.

---

**Made with ❤️ for hardware testing automation**
