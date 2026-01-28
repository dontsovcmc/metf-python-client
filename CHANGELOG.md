# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2] - 2026-01-28

### Added
- RGB LED control functions (`rgb_begin`, `rgb_brightness`, `rgb_color`)
- ESP32C6 Super Mini board support with pin definitions
- Serial port sniffing functionality (`serial_begin`, `serial_read`, `serial_readlines`)
- `serial_readlines()` with delimiter and prefix support for parsing serial output
- Build script (build.py)

### Changed
- Improved project packaging with modern pyproject.toml
- Enhanced documentation in English
- Updated setup.py with comprehensive metadata

## [0.1] - 2020-11-05

### Added
- Initial release
- METFClient core functionality for HTTP-based hardware testing
- Digital I/O operations (`pinMode`, `digitalRead`, `digitalWrite`)
- I2C communication support (`i2c_begin`, `i2c_ask`, `i2c_setClock`, `i2c_setClockStretchLimit`)
- NodeMCU and WeMos board pin definitions
- Basic example scripts demonstrating library usage
- Utility functions (`wait_digital`, `blynk`, `delay`)
- MIT License
