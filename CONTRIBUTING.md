# Contributing to METF Python Client

Thank you for your interest in contributing to METF Python Client! This document provides guidelines and instructions for contributing to the project.

---

## Table of Contents

- [Types of Contributions](#types-of-contributions)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Publishing to PyPI](#publishing-to-pypi)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

---

## Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues in existing code
- **New features**: Add new functionality to the library
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Examples**: Create new examples demonstrating library usage
- **Board support**: Add pin definitions for new ESP boards

---

## Development Setup

### 1. Fork and Clone the Repository

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/metf-python-client.git
cd metf-python-client

# Add upstream remote
git remote add upstream https://github.com/dontsovcmc/metf-python-client.git
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Option 1: Install package in development mode with dev dependencies
pip install -e .[dev]

# Option 2: Install from requirements_dev.txt (recommended)
pip install -r requirements_dev.txt
pip install -e .

# Option 3: Install dependencies manually
pip install -e .
pip install pytest pytest-cov black flake8 mypy build twine wheel
```

**Note:** `requirements_dev.txt` includes all tools needed for development, testing, and publishing.

### 4. Verify Installation

```bash
# Check that metf_python_client is installed
python -c "from metf_python_client import METFClient; print('Installation successful!')"
```

---

## Code Style

### Follow PEP 8

This project follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines for Python code.

### Formatting with Black

Use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format all Python files
black metf_python_client/

# Check formatting without making changes
black --check metf_python_client/
```

### Linting with Flake8

Use [Flake8](https://flake8.pycqa.org/) to check code quality:

```bash
# Run flake8
flake8 metf_python_client/

# With specific settings
flake8 --max-line-length=88 --extend-ignore=E203 metf_python_client/
```

### Type Checking with Mypy

Use [Mypy](http://mypy-lang.org/) for static type checking:

```bash
# Run mypy
mypy metf_python_client/
```

### Pre-commit Hooks (Optional)

You can set up pre-commit hooks to automatically format and check code:

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=metf_python_client tests/

# Run specific test file
pytest tests/test_core.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix: `test_feature.py`
- Name test functions with `test_` prefix: `def test_function_name():`
- Use descriptive test names that explain what is being tested
- Mock HTTP requests when testing METFClient methods

Example test:

```python
import unittest
from metf_python_client import METFClient

class TestMETFClient(unittest.TestCase):
    def test_ping(self):
        # Mock the HTTP request and test ping functionality
        pass
```

---

## Publishing to PyPI

**Note**: Only maintainers with PyPI access can publish new versions.

### Prerequisites

1. **PyPI Account**: Create account at [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. **TestPyPI Account** (optional but recommended): [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
3. **API Token**: Generate API token from PyPI account settings
4. **Required Tools**: Install `build`, `twine`, and `wheel`

```bash
# Install from requirements_dev.txt (includes all publishing tools)
pip install -r requirements_dev.txt

# Or install manually
pip install build twine wheel
```

### Publishing Steps

#### Step 1: Prepare for Release

1. **Update Version Number**

   Edit `metf_python_client/__init__.py`:

   ```python
   VERSION_MAJOR = 0
   VERSION_MINOR = 3  # Increment this
   ```

2. **Update CHANGELOG.md**

   Add new version section with changes:

   ```markdown
   ## [0.3] - 2026-02-15

   ### Added
   - New feature description

   ### Fixed
   - Bug fix description

   ### Changed
   - Changes description
   ```

3. **Commit Changes**

   ```bash
   git add metf_python_client/__init__.py CHANGELOG.md
   git commit -m "Bump version to 0.3"
   ```

4. **Create Git Tag**

   ```bash
   git tag -a v0.3 -m "Release version 0.3"
   git push origin master
   git push origin v0.3
   ```

#### Step 2: Clean Previous Builds

```bash
# Remove old build artifacts
rm -rf dist/ build/ *.egg-info/
```

#### Step 3: Build the Package

```bash
# Build source distribution and wheel
python -m build
```

This creates files in `dist/`:
- `metf-python-client-0.3.tar.gz` (source distribution)
- `metf_python_client-0.3-py3-none-any.whl` (wheel)

#### Step 4: Check the Build

```bash
# Verify package integrity
twine check dist/*
```

Expected output:
```
Checking dist/metf-python-client-0.3.tar.gz: PASSED
Checking dist/metf_python_client-0.3-py3-none-any.whl: PASSED
```

#### Step 5: Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*
```

Enter your TestPyPI API token when prompted.

**Test the Installation:**

```bash
# Create a new virtual environment for testing
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ metf-python-client

# Test that it works
python -c "from metf_python_client import METFClient; print('Test successful!')"

# Deactivate and remove test environment
deactivate
rm -rf test_env
```

#### Step 6: Publish to Production PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

Enter your PyPI API token when prompted.

**Verify Publication:**

- Visit [https://pypi.org/project/metf-python-client/](https://pypi.org/project/metf-python-client/)
- Check that new version appears
- Verify README renders correctly

#### Step 7: Post-Release Tasks

1. **Create GitHub Release**

   - Go to [Releases](https://github.com/dontsovcmc/metf-python-client/releases)
   - Click "Draft a new release"
   - Select the tag you created (v0.3)
   - Copy changelog entries to release notes
   - Publish release

2. **Announce the Release** (optional)

   - Post on project channels
   - Update documentation if needed
   - Notify users of significant changes

### Using API Tokens

For security, use API tokens instead of passwords.

#### Configure .pypirc (Optional)

Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR_API_TOKEN_HERE

[testpypi]
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

**Security Note**: Keep this file secure! Add it to `.gitignore` if in project directory.

#### Using Tokens in Commands

Alternatively, pass token directly:

```bash
twine upload -u __token__ -p pypi-YOUR_TOKEN_HERE dist/*
```

Or set environment variable:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
twine upload dist/*
```

### Troubleshooting

#### "File already exists"

PyPI doesn't allow reuploading the same version. Solutions:

- Increment version number
- Delete `dist/` and rebuild
- Use a post-release version (e.g., 0.3.post1)

#### "Invalid distribution file"

Check:

```bash
twine check dist/*
```

Common issues:
- Missing README.md
- Invalid pyproject.toml syntax
- Broken MANIFEST.in patterns

#### "Package upload failed"

- Verify API token is correct
- Check network connection
- Ensure you have upload permissions
- Try uploading one file at a time:

```bash
twine upload dist/metf-python-client-0.3.tar.gz
twine upload dist/metf_python_client-0.3-py3-none-any.whl
```

#### README not rendering on PyPI

- Ensure `long_description_content_type='text/markdown'` in setup.py
- Check README.md has valid Markdown syntax
- Verify README.md is included in MANIFEST.in

---

## Pull Request Process

### 1. Create a Feature Branch

```bash
# Update master branch
git checkout master
git pull upstream master

# Create feature branch
git checkout -b feature/my-new-feature
```

### 2. Make Your Changes

- Write clean, readable code
- Follow code style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add support for ESP32-S3 board

- Add pin definitions for ESP32-S3
- Update documentation
- Add example for ESP32-S3"
```

**Commit Message Format:**

```
Brief summary (50 chars or less)

Detailed explanation of what changed and why:
- Point 1
- Point 2
- Point 3
```

### 4. Push to Your Fork

```bash
git push origin feature/my-new-feature
```

### 5. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill in the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
Describe how you tested your changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
```

5. Submit the pull request

### 6. Code Review

- Address feedback from reviewers
- Make requested changes
- Push updates to your branch (PR updates automatically)

### 7. Merge

Once approved, a maintainer will merge your PR.

---

## Reporting Issues

### Bug Reports

When reporting bugs, include:

1. **Environment Information**
   - Python version
   - metf-python-client version
   - Operating system
   - ESP board type and firmware version

2. **Steps to Reproduce**
   - Minimal code example
   - Expected behavior
   - Actual behavior

3. **Error Messages**
   - Full error traceback
   - Log output

**Example Bug Report:**

```markdown
**Environment:**
- Python: 3.10
- metf-python-client: 0.2
- OS: Ubuntu 22.04
- ESP: NodeMCU with METF v1.0

**Description:**
i2c_ask() raises exception when response_length > 32

**Code to Reproduce:**
```python
from metf_python_client import METFClient
api = METFClient('192.168.1.100')
api.i2c_begin()
response = api.i2c_ask(0x48, '\x00', 64)  # Fails
```

**Error:**
```
HTTP Error (500): Buffer overflow
```

**Expected:**
Should read 64 bytes successfully
```

### Feature Requests

When requesting features, include:

1. **Use Case**: Why is this feature needed?
2. **Proposed API**: How should it work?
3. **Alternatives**: Have you considered alternatives?
4. **Additional Context**: Any other relevant information

---

## Questions?

If you have questions about contributing:

- Open an issue with the "question" label
- Email the maintainer: don-and-home@mail.ru
- Check existing issues and pull requests

---

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards others

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to METF Python Client!**
