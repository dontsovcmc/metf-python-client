# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

METF Python Client is an HTTP client library for testing hardware using ESP boards (NodeMCU, WeMos, ESP32C6). It enables hardware testing through HTTP requests by communicating with ESP boards running METF firmware, making it ideal for Continuous Integration in hardware development.

The library provides Python bindings for controlling GPIO pins, I2C communication, serial port sniffing, and RGB LED control on remote ESP boards via HTTP API.

## Development Commands

### Installation

```bash
# Install package in development mode
pip install -e .

# Install with development dependencies (recommended)
pip install -r requirements_dev.txt
pip install -e .

# OR install with dev extras
pip install -e .[dev]
```

### Testing

```bash
# Run all tests (if tests directory exists)
pytest tests/

# Run with coverage
pytest --cov=metf_python_client tests/

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Format code with Black
black metf_python_client/

# Check formatting without changes
black --check metf_python_client/

# Lint with Flake8
flake8 metf_python_client/
flake8 --max-line-length=88 --extend-ignore=E203 metf_python_client/

# Type checking with Mypy
mypy metf_python_client/
```

### Building and Publishing

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build package
python -m build

# Check build integrity
twine check dist/*

# Upload to TestPyPI (testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

## Publishing New Version to PyPI

When the user asks to publish a new version to PyPI, follow these steps:

### Step 1: Update Version Number

1. Read `metf_python_client/_version.py`
2. Increment `VERSION_MINOR` (or `VERSION_MAJOR` for breaking changes)
3. Save the updated version file

Example: If current version is 0.3, update to 0.4:
```python
VERSION_MAJOR = 0
VERSION_MINOR = 4  # Incremented from 3
```

### Step 2: Update CHANGELOG.md

1. Read `CHANGELOG.md`
2. Add a new section at the top with the new version and current date
3. Document the changes made (Added, Fixed, Changed, Removed sections as appropriate)
4. Save the updated changelog

Example format:
```markdown
## [0.4] - 2026-01-28

### Added
- Description of new features

### Fixed
- Description of bug fixes

### Changed
- Description of changes
```

### Step 3: Commit Changes and Create Git Tag

```bash
# Stage version and changelog files
git add metf_python_client/_version.py CHANGELOG.md

# Commit the version bump
git commit -m "Bump version to 0.4"

# Create annotated git tag
git tag -a v0.4 -m "Release version 0.4"

# Push commit and tag to remote
git push origin master
git push origin v0.4
```

### Step 4: Clean and Build Package

```bash
# Remove any previous build artifacts
rm -rf dist/ build/ *.egg-info/

# Build source distribution and wheel
python -m build
```

This creates two files in `dist/`:
- `metf-python-client-0.4.tar.gz` (source distribution)
- `metf_python_client-0.4-py3-none-any.whl` (wheel)

### Step 5: Verify Build

```bash
# Check package integrity
twine check dist/*
```

Expected output: Both files should show "PASSED"

### Step 6: Upload to PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

The user will need to provide their PyPI API token when prompted, or it should be configured in `~/.pypirc`.

### Step 7: Verify Publication

After upload completes:
1. Visit https://pypi.org/project/metf-python-client/ to verify new version appears
2. Check that README renders correctly on PyPI page
3. Confirm version badge shows correct version

### Optional: Test on TestPyPI First

For major changes, test on TestPyPI before production:

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ metf-python-client

# If successful, proceed with production upload
twine upload dist/*
```

### Important Notes

- **Version file location**: `metf_python_client/_version.py`
- **Changelog location**: `CHANGELOG.md` (in repository root)
- **Cannot re-upload**: PyPI doesn't allow uploading the same version twice. If upload fails, must increment version again.
- **Git tag format**: Use `v` prefix (e.g., `v0.4`, not `0.4`)
- **Main branch**: `master` (not `main`)

## Architecture

### Core Components

**METFClient (`metf_python_client/core.py`)**
- Main client class that communicates with ESP boards via HTTP
- Uses `requests.Session` for connection management
- All methods send HTTP GET/POST requests to ESP board endpoints
- Handles GPIO operations (pinMode, digitalRead, digitalWrite)
- Handles I2C operations (begin, ask, setClock, setClockStretchLimit, flush)
- Handles serial operations (begin, read, readlines, flush)
- Handles RGB LED operations (begin, brightness, color)

**Board Definitions (`metf_python_client/boards/`)**
- Pin mappings and constants for different ESP boards
- `nodemcu.py`: NodeMCU (ESP8266) pin definitions (D0-D10, LED_BUILTIN, etc.)
- `wemos.py`: WeMos D1 Mini pin definitions (D0-D8, LED_BUILTIN, etc.)
- `esp32c6_super_mini.py`: ESP32C6 Super Mini pin definitions (IO0-IO23, LED_BUILTIN, etc.)
- Each board module defines HIGH/LOW, INPUT/OUTPUT/INPUT_PULLUP constants

**Utilities (`metf_python_client/utils.py`)**
- `DataStruct`: Class for parsing binary data from I2C responses using struct format
- `str2hex()`: Convert hex string to ASCII characters ('303132' → '123')
- `hex2str()`: Convert ASCII string to hex representation ('123' → '303132')
- `str2array()`: Convert hex string to bytearray

**Logging (`metf_python_client/logger.py`)**
- Centralized logging configuration for debugging HTTP requests and responses

### Data Flow

1. User creates `METFClient(host, port)` instance
2. User calls API method (e.g., `api.digitalWrite(pin, value)`)
3. METFClient sends HTTP request to ESP board at `http://host:port/endpoint`
4. ESP board (running METF firmware) executes hardware operation
5. ESP board returns HTTP response
6. METFClient validates response and returns result to user

### I2C Communication Pattern

The I2C implementation has a specific flow:
1. Initialize with `i2c_begin(sda, scl)` - sets up I2C pins
2. Optionally configure with `i2c_setClock()` and `i2c_setClockStretchLimit()`
3. Communicate using `i2c_ask(address, message, response_len)`:
   - Converts message to hex string using `hex2str()`
   - Sends to ESP board which performs I2C transaction
   - Receives hex response and converts back using `str2hex()`
4. Use `DataStruct` class to parse binary responses into structured data

## Version Management

Version is defined in `metf_python_client/_version.py`:
- `VERSION_MAJOR`: Major version number
- `VERSION_MINOR`: Minor version number
- `__version__`: Constructed from MAJOR.MINOR

Update version before publishing:
1. Edit `_version.py` to increment version
2. Update `CHANGELOG.md` with changes
3. Create git tag: `git tag -a v0.X -m "Release version 0.X"`
4. Build and publish to PyPI

## Adding New Board Support

To add support for a new ESP board:
1. Create new file in `metf_python_client/boards/` (e.g., `esp32s3.py`)
2. Define pin mappings for the board (map board labels to GPIO numbers)
3. Include HIGH/LOW and INPUT/OUTPUT/INPUT_PULLUP constants
4. Add comments documenting special pin behaviors (boot modes, pulled pins, etc.)
5. Update README.md with board documentation
6. Add board to pyproject.toml packages list if needed

## HTTP API Endpoints

The ESP board firmware provides these endpoints:
- `/ping` - Test connectivity (returns 'pong')
- `/version` - Get firmware version
- `/pinMode` - Set pin mode (POST: pin, mode)
- `/digitalRead` - Read digital pin value (GET: pin)
- `/digitalWrite` - Write digital pin value (POST: pin, value)
- `/i2c` - I2C operations (POST: action, parameters)
- `/serial` - Serial port operations (POST/GET: various parameters)
- `/rgb` - RGB LED control (POST: action, parameters)
- `/read` - Read serial data (GET)

## Project Structure

```
metf_python_client/
├── core.py                 # Main METFClient class
├── utils.py                # Utility functions (hex conversion, DataStruct)
├── logger.py               # Logging configuration
├── _version.py            # Version information
├── __init__.py            # Package exports
├── boards/                 # Board-specific pin definitions
│   ├── nodemcu.py
│   ├── wemos.py
│   └── esp32c6_super_mini.py
└── examples/               # Usage examples
    ├── 01-Blynk.py
    ├── 02-CheckButton.py
    ├── 03-BlynkUnitTest.py
    ├── 04-ButtonUnitTest.py
    ├── 05-i2c.py
    └── 06-RGBLed.py
```
